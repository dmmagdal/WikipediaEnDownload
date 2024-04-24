# download.py
# Download parts of or all of the latest English wikipedia data from 
# their archive.
# Python 3.7
# Windows/MacOS/Linux


import argparse
import requests
from bs4 import BeautifulSoup


def main():
    # Set up argument parser.
    parser = argparse.ArgumentParser()

    # Core URL to latest dump of wikipedia.
    url = "https://dumps.wikimedia.org/enwiki/latest/"

    # Different mappings of URLs to data.
    url_mapping = {
        "all": "pages-articles-multistream.xml.bz2",    # Current revisions only, no talk or user pages; this is probably what you want, and is over 19 GB compressed (expands to over 86 GB when decompressed).
        "pages-meta": "pages-meta-current.xml.bz2",     # Current revisions only, all pages (including talk)
        "abstracts": "abstract.xml.gz",                 # Page abstracts
        "article-titles": "all-titles-in-ns0.gz"        # Article titles only (with redirects)
    }

    # Query the download page.
    response = requests.get(url)

    # Set up BeautifulSoup object.
    soup = BeautifulSoup(response.text, "lxml")

    # Exit the program.
    exit(0)


if __name__ == '__main__':
    main()