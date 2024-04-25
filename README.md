# Wikipedia English Dataset Download

Description: Provides an interesting look at downloading and processing Wikipedia (English only)


### Setup

 - Use either the dockerfile or a virtual environment to setup the necessary environment to run the files.
 - Python virtual environment (venv)
     - Initialize: `python -m venv wiki-download`
     - Activate: 
        - Windows: `/wiki-download/Scripts/activate`
        - Linux/MacOS: `source /wiki-download/bin/activate`
     - Install dependencies: `pip install -r requirements.txt`
 - Docker
     - The dockerfile is primarily for downloading the current revision of wikipedia (`pages-articles-multistream.xml.bz2`). The arguments for the download script are fixed so you will have to edit the dockerfile to whatevery arguments you desire.
     - Build: `docker build -t wiki-download -f Dockerfile .`
     - Run: `docker run -v {$pwd}:/wiki wiki-download`


### Usage

 - Lorem ipsum



### References

 - The [size of wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia)
 - Wikipedia [statistics](https://en.wikipedia.org/wiki/Wikipedia:Statistics)
 - Wikipedia [database download](https://en.wikipedia.org/wiki/Wikipedia:Database_download)
 - Wikipedia [dumps home page](https://dumps.wikimedia.org/)
 - [English wikipedia dumps](https://dumps.wikimedia.org/enwiki/) in SQL and XML
     - pages-articles-multistream.xml.bz2 –> Current revisions only, no talk or user pages; this is probably what you want, and is over 19 GB compressed (expands to over 86 GB when decompressed).
     - pages-meta-current.xml.bz2 –> Current revisions only, all pages (including talk)
     - abstract.xml.gz –> page abstracts
     - all-titles-in-ns0.gz –> Article titles only (with redirects)
     - SQL files for the pages and links are also available
     - All revisions, all pages: These files expand to multiple terabytes of text. Please only download these if you know you can cope with this quantity of data. Go to Latest Dumps and look out for all the files that have 'pages-meta-history' in their name.
 - BeautifulSoup [documentation](https://beautiful-soup-4.readthedocs.io/en/latest/)
 - Documentation of native python module used:
     - [argparse](https://docs.python.org/3.9/library/argparse.html)
     - [bz2](https://docs.python.org/3.9/library/bz2.html)
     - [gzip](https://docs.python.org/3.9/library/gzip.html)
     - [hashlib](https://docs.python.org/3.9/library/hashlib.html)
     - [os](https://docs.python.org/3.9/library/os.html)