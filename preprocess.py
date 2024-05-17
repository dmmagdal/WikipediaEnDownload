# preprocess.py
# Extract and preprocess the downloaded compressed files containing the
# latest English wikipedia data from the downloads folder.
# Python 3.9
# Windows/MacOS/Linux


import argparse
import bz2
import copy
import gzip
import hashlib
import os
from bs4 import BeautifulSoup


def main():
	# Set up argument parser.
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"target", 
		nargs="?",
		default="abstracts", 
		help="Specify which (compressed) file(s) you want to extract. Default is 'abstracts'."
	)
	parser.add_argument(
		"--shard",
		action="store_true",
		help="Specify whether to download the whole (compressed) file or the file in shards. Default is false/not specified."
	)
	parser.add_argument(
		"--no_clean",
		action="store_false",
		help="Specify whether to delete the decompressed file(s) once the preprocessing is done. Default is true/not specified."
	)
	args = parser.parse_args()

	###################################################################
	# CONSTANTS
	###################################################################
	# Different mappings of targets to files.
	target_mapping = {
		"all": "pages-articles-multistream.xml.bz2",	# Current revisions only, no talk or user pages; this is probably what you want, and is over 19 GB compressed (expands to over 86 GB when decompressed).
		"pages-meta": "pages-meta-current.xml.bz2",		# Current revisions only, all pages (including talk)
		"abstracts": "abstract.xml.gz",             	# Page abstracts
		# "article-titles": "all-titles-in-ns0.gz",   	# Article titles only (with redirects)
		# "sha1sum": "enwiki-latest-sha1sums.txt",					# Sha1sums for latest wikis
	}

	# NOTE:
	# -> Target "article-titles" is not supported (not able to
	#	decompress manually).
	# -> Target "sha1sum" is not supported (it's a text file containing
	#	the SHA1SUM for the other compressed files).

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
	base_name = os.path.splitext(
		os.path.splitext(os.path.basename(base_file))[0]	# gives base_name.xml
	)[0]													# gives base_name
	local_filepath = [os.path.join(folder, base_file)]

	if args.shard:
		local_filepath = [
			os.path.join(folder, file) for file in os.listdir(folder)
			if base_name in file and len(file) != len(base_file)
		]

	# Verify target filepath(s) exists.
	if len(local_filepath) == 1 and not os.path.exists(local_filepath[0]):
		print(f"Target file {local_filepath} was not found.")
		exit(1)
	elif len(local_filepath) == 0:
		print(f"Shards for target file {local_filepath} were not found.")
		exit(1)

	# Folder and file path for output data files.
	output_folder = "./WikipediaData"
	if not os.path.exists(output_folder) or not os.path.isdir(output_folder):
		os.makedirs(output_folder, exist_ok=True)

	# Confirm file decompression.
	print("WARNING!")
	print("The compressed files downloaded can be as large as 100GB when decompressed. Please make sure you have enough disk space before proceeding.")
	confirmation = input("Proceed? [Y/n] ")
	if confirmation not in ["Y", "y"]:
		exit(0)

	# Iterate through the list of file paths.
	for filepath in local_filepath:
		###############################################################
		# DECOMPRESSION
		###############################################################
		# Verify that the target file path is a supported compression
		# format.
		if not filepath.endswith(".gz") and not filepath.endswith(".bz2"):
			print(f"Target compressed file path {filepath} is not in a supported by this script. Supporting only '.bz2' and '.gz' compressed files only.")
			exit(0)

		# Decompress the compressed file (if necessary).
		decompressed_filepath = filepath.rstrip(".gz").rstrip(".bz2")
		if not os.path.exists(decompressed_filepath):
			if filepath.endswith(".gz"):
				decompress_gz(filepath)
			elif filepath.endswith(".bz2"):
				decompress_bz2(filepath)

		###############################################################
		# PROCESSING
		###############################################################
		# Set the output filepath. For the filepath, use the file base 
  		# name without the extension. We are using this as a base for
		# each file we will create in preprocessing.
		output_filepath = os.path.join(
			output_folder, 
			os.path.splitext(os.path.basename(decompressed_filepath))[0]
		)

		# NOTE:
		# -> for abstracts, you can split each abstract into documents 
		#	by <doc> tag.
		# -> for the pages-articles-multistream, you can split each 
		#	page into documents by the <page> tag.
		# Open the decompressed (xml) file and split each entry in the 
		# file to its own xml file.
		split_into_documents(decompressed_filepath, output_filepath)

		###############################################################
		# CLEAN UP
		###############################################################
		# Use command line arguments on whether to delete the
		# decompressed copies of the compressed files.
		if args.no_clean:
			# Delete the decompressed copies for the compressed files.
			print("Deleting decompressed files...")
			files = [
				os.path.join(folder, file) for file in os.listdir(folder) 
				if not file.endswith(".bz2") and not file.endswith(".bz")
			]
			for file in files:
				os.remove(file)
				print(f"Deleted {file}")

	print("Completed decompression and preprocessing.")

	# Exit the program.
	exit(0)


def decompress_bz2(local_filepath: str) -> None:
	"""
	Decompress/extract the bz2 file.
	@param: local_filepath (str), the local path to the compressed bz2 file.
	@return: returns nothing.
	"""
	# The output filepath.
	output_filepath = local_filepath.rstrip(".bz2")

	# Perform the decompression.
	with open(local_filepath, 'rb') as f_in:
		with open(output_filepath, 'wb') as f_out:
			f_out.write(bz2.decompress(f_in.read()))

	# Assert the decompress file was created.
	assert os.path.exists(output_filepath), f"Decompression failed. Output {output_filepath} file was not created."

	return


def decompress_gz(local_filepath: str) -> None:
	"""
	Decompress/extract the bz2 file.
	@param: local_filepath (str), the local path to the compressed bz2 file.
	@return: returns nothing.
	"""
	# The output filepath.
	output_filepath = local_filepath.rstrip(".gz")
	
	# Perform the decompression.
	with gzip.open(local_filepath, 'rb') as f_in:
		with open(output_filepath, 'wb') as f_out:
			f_out.write(f_in.read())

	# Assert the decompress file was created.
	assert os.path.exists(output_filepath), f"Decompression failed. Output {output_filepath} file was not created."

	return


def split_into_documents(local_filepath: str, output_filepath: str) -> None:
	"""
	Split the decompressed large xml file into smaller xml files that
		are for individual pages/articles.
	@param: local_filepath (str), the local path to the decompressed 
		xml file.
	@param: output_filepath (str), the output local path to the decompressed 
		xml file.
	@return: returns nothing.
	"""
	# Load the (xml) file contents.
	with open(local_filepath, "r") as f:
		file_contents = f.read()

	# Use beautifulsoup to parse the (xml) file into multiple files for
	# each entry. For the abstract, each entry is split by <doc> tag
	# and for pages, each entry is split by <page> tag.
	soup = BeautifulSoup(file_contents, "lxml")
	docs = soup.find_all("doc")
	pages =  soup.find_all("page")

	# Assign a list of found elements (<docs> or <pages>) depending on
	# what was picked up but beautifulsoup. If neither or both are
	# found then we return early.
	list_elements = None
	if len(docs) == 0 and len(pages) > 0:
		# Process the page.
		list_elements = copy.deepcopy(pages)
	elif len(pages) == 0 and len(docs) > 0:
		# Process the abstract.
		list_elements = copy.deepcopy(docs)
	else:
		# Return early. Accounts for no abstracts and pages or there
		# are both abstracts and pages.
		return
	
	# NOTE:
	# -> Chunk size 250_000 resulted in output files that were above 
	#	the 1 GB file limit set by the design specs. 
	# -> Chunk size of 200_000 resulted in an OOM error (for some 
	#	reason).
	# -> Chunk size of 150_000 resulted in almost all of the output
	#	xml files with the exception of 1 that was only 1.6 GB. At the
	#	time of writing this, it may not be a big deal for the JS 
	#	implementation of the search engine, but this can be confirmed
	#	later.
	# -> Chunk size of 100_000 was quite below the threshold.
	# TODO:
	# Verify that the preprocessed (decompressed xml) file(s) over 1GB
	# in size are able to be read and further preprocessed by the 
	# search engine in the JS implementation. If so, adjust the chunk
	# size to 125_000 or 100_000 and rerun to confirm that all the xml
	# files are under the 1GB limit.

	# Iterate through the list of elements and chunk the list.
	chunk_size = 150_000
	for idx in range(0, len(list_elements), chunk_size):
		# For each chunk, convert the data to a string.
		chunk = list_elements[idx:idx + chunk_size]
		chunk_str = "".join(str(element) for element in chunk)
		chunk_prettified = BeautifulSoup(chunk_str, "lxml").prettify()

		# Compute the hash of the raw xml string.
		hash = hashSum(chunk_str)

		# Finalize the file output path.
		file = output_filepath + "_" + hash + ".xml"

		# Write the page in the output path.
		with open(file, "w+") as f:
			f.write(chunk_prettified)
		
		print(f"Created {file}")
	
	# Iterate through each element, storing it to a file.
	# for element in list_elements:
	# 	# Convert the element to a string.
	# 	element_str = str(element)

	# 	# Compute the hash of the raw xml string.
	# 	hash = hashSum(element_str)

	# 	# Finalize the file output path.
	# 	file = output_filepath + "_" + hash + ".xml"

	# 	# Write the page in the output path.
	# 	with open(file, "w+") as f:
	# 		f.write(element.prettify())
		
	# 	print(f"Created {file}")
	
	return


def hashSum(data: str) -> str:
	"""
	Compute the SHA256SUM of the xml data. This is used as part of the
		naming scheme down the road.
	@param: data (str), the raw string data from the xml data.
	@return: returns the SHA256SUM hash.
	"""

	# Initialize the SHA256 hash object.
	sha256 = hashlib.sha256()

	# Update the hash object with the (xml) data.
	sha256.update(data.encode('utf-8'))

	# Return the digested hash object (string).
	return sha256.hexdigest()


if __name__ == '__main__':
	main()