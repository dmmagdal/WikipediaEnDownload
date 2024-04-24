# Wikipedia English Dataset Download

Description: Provides an interesting look at downloading Wikipedia (English only)


### Setup

 - Python virtual environment (venv)
 - Docker


### Usage

 - Lorem ipsum


### References

 - The [size of wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia)
 - Wikipedia [statistics](https://en.wikipedia.org/wiki/Wikipedia:Statistics)
 - Wikipedia [database download](https://en.wikipedia.org/wiki/Wikipedia:Database_download)
 - [English wikipedia dumps](https://dumps.wikimedia.org/enwiki/) in SQL and XML
     - pages-articles-multistream.xml.bz2 –> Current revisions only, no talk or user pages; this is probably what you want, and is over 19 GB compressed (expands to over 86 GB when decompressed).
     - pages-meta-current.xml.bz2 –> Current revisions only, all pages (including talk)
     - abstract.xml.gz –> page abstracts
     - all-titles-in-ns0.gz –> Article titles only (with redirects)
     - SQL files for the pages and links are also available
     - All revisions, all pages: These files expand to multiple terabytes of text. Please only download these if you know you can cope with this quantity of data. Go to Latest Dumps and look out for all the files that have 'pages-meta-history' in their name.
 - Latest BeautifulSoup [documentation](https://beautiful-soup-4.readthedocs.io/en/latest/)