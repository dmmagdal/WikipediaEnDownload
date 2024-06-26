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

 - Download Wikipedia data (`download.py`)
     - `python download.py [target] --shard --no_shasum`
     - `--shard`: Specify whether to download the `[target]` via its shards or the entire original file
     - `--no_shasum`: Specify whether to verify the download(s) with the SHA1SUM
 - Preprocess the downloaded Wikipedia data (`preprocess.py`)
     - `python preprocess.py [target] --shard --no_clean`
     - `--shard`: Specify whether to decompress the `[target]` via its shards or the entire original file
     - `--no_clean`: Specify whether to remove all decompressed files from the file system
 - For best results
     - `python download.py all --shard --no_shasum`
     - `python preprocess.py all --shard`


### Notes

 - You cannot decompress a compressed file whose decompressed size is greater than the system's memory (RAM). This means there are some system requirements to download and extract this data.
     - Minimum system storage and memory requirements for each file: 
         - pages-articles-multistream.xml.bz2
             - 19+ GB disk space compressed
             - 86+ GB disk space decompressed
             - Expect to use at least 64+ GB of RAM for the decompression
         - pages-meta-current.xml.bz2
             - XX+ GB disk space compressed
             - XX+ GB disk space decompressed
             - Expect to use at least XX+ GB of RAM for the decompression
         - abstract.xml.gz
             - 850+ MB disk space compressed
             - 6.6+ GB disk space decompressed
             - Expect to use at least 8 GB of RAM for the decompression
     - It is advised for the "pages" downloads that you use the shard flag. This will download each piece in shards (the data is broken up into shards on the main link) and process the shards accordingly. This uses significantly less RAM than downloading the entire compressed file and allows for multiprocessing.
         - In this [blog post](https://blog.online-convert.com/what-are-tar-gz-and-bz2/), gz (gzip) is faster and more memory efficent while bz2 (bzip2) is slower but produces smaller compressed files. All pages are saved in bz2 compressed files to maximize compression.
         - You may want to pass `--no_shasum` to the download script because 1 of the compressed files does not have an entry in the SHA1SUM list online. This may have adverse affects if other files are downloaded but do not have matching SHA1SUM.
 - Preprocessing consists of the following:
     - Decompress the compressed file
         - See decompression details above.
     - For each decompressed file, extract a chunk of articles and store them to an xml file.
         - This was revised from the 1 article to 1 xml file strategy, which produced A LOT of files but resulted in running out of storage. 
             - The working theory is that the overhead of creating each file scaled with the number of articles, which was in the millions when the 256GB external drive ran out of space. 
             - This should also make it easier to clear the files when you need to free up space. Takes less time to purge a few larger files than several smaller ones.
             - Another benefit is that with fewer files to create, the preprocessing should go faster. File IO is a costly operation so performing this a few hundred times vs millions of times is a massive time saver.
             - The chunk size was arbitrarily determined based on the number of articles per compressed file while also balancing the size of the expected xml file (each file should be under 1GB so that it can be handled in NodeJS).
                 - Note that according to the NodeJS documentation (as of [v18](https://nodejs.org/docs/v18.0.0/api/buffer.html#buffer-constants) to [v22](https://nodejs.org/api/buffer.html#buffer-constants) which is current latest version), the buffer threshold is 1GB on 32-bit systems or 4GB on 64-bit systems ([v14](https://nodejs.org/docs/v14.0.0/api/buffer.html#buffer_buffer_constants) has a threshold of 2GB on 64-bit systems).
                 - Sources on maximum buffer sizes for loading files:
                     - Processing large file and nodes and memory limit in nodejs [stackoverflow](https://stackoverflow.com/questions/63553223/processing-large-file-and-nodes-and-memory-limit-in-nodejs#:~:text=Node%20documentation%20states%20the%20maximum,js.)
                     - What's the maximum size of a Node.js Buffer [stackoverflow](https://stackoverflow.com/questions/8974375/whats-the-maximum-size-of-a-node-js-buffer#:~:text=Maximum%20length%20of%20a%20typed,2Gb%20%2D%201byte%20on%2064%2Dbit)
                     - Parsing large xml files (1G+) in node.js [stackoverflow](https://stackoverflow.com/questions/52314871/parsing-large-xml-files-1g-in-node-js)
         - This part may take up a lot of space. It is recommended that the whole process is done on a cheap external drive with a lot of storage capacity.
     - Delete the decompressed file (optional)
         - It is highly recommended that clean up is done to keep things running smoothly on the system.
 - Parsing documents
     - For pages-articles-multistream.xml files, each entry is contained within `<page>` tags.
     - For abstract.xml.gz, each entry is contained with `<doc>` tags.
     - Within either of the preprocessed xml files, the tag with the most data is going to be the `<title>` and `<text>` tags. The `<links>` tag is also useful for constructing graphs or additional knowledge. Note that the text in the `<text>` tag may not be well formatted.
 - Preprocessing output notes
     - Chunked at 150,000 entries per file. Resulted in a few files larger than the 1 GB limit set be the spec. These files were primarily in the first 10 bz2 bundles (2, 3, 4, 5, 6).
         - I can try again at 125,000 or 100,000 entries per file but that will probably balloon the number of files used (so that's another thing to consider).
         - File(s) with the most offensive file size is 1.6 GB.
     - Decompressed output files uses 95 GB in storage and created almost 200 files (195 to be exact).
     - It took around 22 hours to complete the preprocessing.
         - real	1314m30.630s
         - user	1210m54.350s
         - sys	100m25.085s
     - Ran processing on my server for the sake of speed. Server had 64GB of RAM and 56 cores but the program was using a single thread/processor. Almost all of the 64GB of RAM was utilized (I suspect for the decompression step in preprocessing). Still, no special hardware is really needed outside of the required memory. Project is still able to run on "consumer hardware" for anyone to repeat/replicate.
 - Link to dataset on Huggingface:
     - [compressed xml files](https://huggingface.co/datasets/dmmagdal/enwiki-2024-04-20)
     - [chunked decompressed xml files](https://huggingface.co/datasets/dmmagdal/enwiki-2024-04-20-xml)


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
     - Alternative English Wikipedia dump ([cirrussearch](https://dumps.wikimedia.org/other/cirrussearch/current/))
         - Use enwiki-\[DATE\]-cirrussearch-content.json.gz
         - Is 40 GB all compressed
         - Downloader currently not implemented in this repo
 - BeautifulSoup [documentation](https://beautiful-soup-4.readthedocs.io/en/latest/)
 - Documentation of native python module used:
     - [argparse](https://docs.python.org/3.9/library/argparse.html)
     - [bz2](https://docs.python.org/3.9/library/bz2.html)
     - [copy](https://docs.python.org/3.9/library/copy.html)
     - [gzip](https://docs.python.org/3.9/library/gzip.html)
     - [hashlib](https://docs.python.org/3.9/library/hashlib.html)
     - [os](https://docs.python.org/3.9/library/os.html)