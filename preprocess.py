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

    return


if __name__ == '__main__':
    main()