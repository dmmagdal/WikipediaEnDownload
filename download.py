# download.py
# Download parts of or all of the latest English wikipedia data from 
# their archive.
# Python 3.9
# Windows/MacOS/Linux


import argparse
import hashlib
import os
from bs4 import BeautifulSoup
import requests


def main():
	# Set up argument parser.
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"target", 
		nargs="?",
		default="abstracts", 
		help="Specify which (compressed) file you want to download. Default is 'abstracts'."
	)
	args = parser.parse_args()

	###################################################################
	# CONSTANTS
	#################################################################### Core URL to latest dump of wikipedia.
	url = "https://dumps.wikimedia.org/enwiki/latest/"

	# Different mappings of targets to files.
	target_mapping = {
		"all": "enwiki-latest-pages-articles-multistream.xml.bz2",  # Current revisions only, no talk or user pages; this is probably what you want, and is over 19 GB compressed (expands to over 86 GB when decompressed).
		"pages-meta": "en-wiki-latest-pages-meta-current.xml.bz2",	# Current revisions only, all pages (including talk)
		"abstracts": "enwiki-latest-abstract.xml.gz",             	# Page abstracts
		"article-titles": "enwiki-latest-all-titles-in-ns0.gz",   	# Article titles only (with redirects)
		"sha1sum": "enwiki-latest-sha1sums.txt",					# Sha1sums for latest wikis
	}
	base_mapping = {
		key: value.lstrip("enwiki-latest-") 
		for key, value in target_mapping.items()
	}	# This is primarily for finding the right SHA1SUM in the SHA1SUM txt file

	# Verify arguments.
	target = args.target
	valid_targets = list(target_mapping.keys())
	if target not in valid_targets:
		print(f"Download argument 'target' {target} not valid target.")
		print(f"Please specify one of the following for the target: {valid_targets}")
		exit(1)

	# Folder and file path for downloads.
	folder = "./CompressedDownloads"
	base_file = target_mapping[target]
	base_name = base_mapping[target]
	local_filepath = os.path.join(folder, base_file)

	if not os.path.exists(folder) or not os.path.isdir(folder):
		os.makedirs(folder, exist_ok=True)
	
	###################################################################
	# QUERY LATEST PAGE TO GET DOWNLOAD URL
	###################################################################
	# Query the download page.
	response = requests.get(url)
	return_status = response.status_code
	if return_status != 200:
		print(f"Resquest returned {return_status} status code for {url}")
		exit(1)

	# Set up BeautifulSoup object.
	soup = BeautifulSoup(response.text, "lxml")

	# Find the necessary link.
	# links = soup.find_all('a')
	# link_element = soup.find("a", text=base_file)
	link_element = soup.find("a", string=base_file)
	if link_element is None:
		print(f"Could not find {base_file} in latest dump {url}")
		exit(1)

	link_url = url + link_element.get("href")

	###################################################################
	# QUERY SHA1SUM
	###################################################################
	# Query the link for the shasums.
	# shasum_element = soup.find("a", text=target_mapping["sha1sum"])
	shasum_element = soup.find("a", string=target_mapping["sha1sum"])
	if shasum_element is None:
		print(f"Could not find {target_mapping['sha1sum']} in latest dump {url}")
		exit(1)

	shasum_url = url + shasum_element.get("href")

	# Extract the necessary shasum from the response.
	shasum_response = requests.get(shasum_url)
	return_status = shasum_response.status_code
	if return_status != 200:
		print(f"Resquest returned {return_status} status code for {shasum_url}")
		exit(1)

	shasum_soup = BeautifulSoup(shasum_response.text, "lxml")
	shasum_text = shasum_soup.get_text()
	shasum_text_lines = shasum_text.split("\n")
	sha1 = ""
	for line in shasum_text_lines:
		if base_name in line:
			sha1 = line.split(" ")[0]
	
	if len(sha1) == 0:
		print(f"Could not find SHA1SUM for {base_file}")
		exit(1)

	###################################################################
	# DOWNLOAD FILE
	###################################################################
	# Initialize the file download,
	print("WARNING!")
	print("The compressed files downloaded can be as large as 25GB each. Please make sure you have enough disk space before proceeding.")
	confirmation = input("Proceed? [Y/n] ")
	if confirmation not in ["Y", "y"]:
		exit(0)

	print(f"Downloading {base_file} file...")
	download_status = downloadFile(link_url, local_filepath, sha1)

	# Verify file download was successful.
	status = "successfully" if download_status else "not sucessfully"
	print(f"Target file {base_file} was {status} downloaded.")

	# Exit the program.
	exit(0)


def downloadFile(url: str, local_filepath: str, sha1: str) -> bool:
	"""
	Download the specific (compressed) file from the wikipedia link.
		Verify that the downloaded file is also correct with SHA1SUM.
	@param: url (str), the URL of the compressed file to download.
	@param: local_filepath (str), the local path the compressed file is
		going to be saved to.
	@param: sha1 (str), the SHA1SUM hash expected for the downloaded 
		file.
	@return: returns a bool of whether that compressed file was 
		successfully downloaded (verified with SHA1SUM).
	"""

	# Open request to the URL.
	with requests.get(url, stream=True) as r:
		# Raise an error if there is an HTTP error.
		r.raise_for_status()

		# Open the file and write the data to the file.
		with open(local_filepath, 'wb+') as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)

	# Return whether the file was successfully created.
	new_sha1 = hashSum(local_filepath)
	print(f"Expected SHA1: {sha1}")
	print(f"Computed SHA1: {new_sha1}")
	return sha1 == new_sha1


def hashSum(local_filepath: str) -> str:
	"""
	Compure the SHA1SUM of the downloaded (compressed) file. This
		confirms if the download was successful.
	@param: local_filepath (str), the local path the compressed file is
		going to be saved to.
	@return: returns the SHA1SUM hash.
	"""

	# Initialize the SHA1 hash object.
	sha1 = hashlib.sha1()

	# Check for the file path to exist. Return an empty string if it
	# does not exist.
	if os.path.exists(local_filepath):
		return ""

	# Open the file.
	with open(local_filepath, 'rb') as f:
		# Read the file contents and update the has object.
		while True:
			data = f.read(8192)
			if not data:
				break
			sha1.update(data)

	# Return the digested hash object (string).
	return sha1.hexdigest()


if __name__ == '__main__':
	main()