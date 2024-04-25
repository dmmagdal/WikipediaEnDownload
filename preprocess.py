# preprocess.py
# Extract and preprocess the downloaded compressed files containing the
# latest English wikipedia data from the downloads folder.
# Python 3.9
# Windows/MacOS/Linux


import argparse
import bz2
import gzip
import os
from bs4 import BeautifulSoup


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
	###################################################################
	# Different mappings of targets to files.
	target_mapping = {
		"all": "enwiki-latest-pages-articles-multistream.xml.bz2",  # Current revisions only, no talk or user pages; this is probably what you want, and is over 19 GB compressed (expands to over 86 GB when decompressed).
		"pages-meta": "en-wiki-latest-pages-meta-current.xml.bz2",	# Current revisions only, all pages (including talk)
		"abstracts": "enwiki-latest-abstract.xml.gz",             	# Page abstracts
		# "article-titles": "enwiki-latest-all-titles-in-ns0.gz",   	# Article titles only (with redirects)
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
	local_filepath = os.path.join(folder, base_file)
	if not os.path.exists(local_filepath):
		print(f"Target file {local_filepath} was not found.")
		exit(1)

	###################################################################
	# DECOMPRESSION
	###################################################################
	# Verify that the target file path is a supported compression
	# format.
	if not local_filepath.endswith(".gz") or not local_filepath.endswith(".bz2"):
		print(f"Target compressed file path {local_filepath} is not in a supported by this script. Supporting only '.bz2' and '.gz' compressed files only.")
		exit(0)

	# Decompress the compressed file (if necessary).
	decompressed_filepath = local_filepath.rstrip(".gz").rstrip(".bz2")
	if not os.path.exists(decompressed_filepath):
		if local_filepath.endswith(".gz"):
			decompress_gz(local_filepath)
		elif local_filepath.endswith(".bz2"):
			decompress_bz2(local_filepath)

	###################################################################
	# PROCESSING
	###################################################################

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


if __name__ == '__main__':
	main()