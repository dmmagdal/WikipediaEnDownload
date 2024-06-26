# Docker file to run a container that will run the download.py in
# Python 3.

# Load the image for Python 3.
FROM python:3.7.19-alpine

# Set locale for variable (pulled from dockerfile in original OpenAI
# GPT2 repository).
ENV LANG=C.UTF-8

# Create a directory in the docker container. Set the working directory
# in the container to that newly created directory and then add all
# files from the current directory in the host to the working directory
# in the container.
RUN mkdir /wiki
WORKDIR /wiki
ADD . /wiki

# Set up a volume so that the current directory in the host is
# connected to the working directory in the container.

# Install all required modules in the requirements.txt file.
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Run the download.py program.
CMD ["python3", "download.py", "all"]
# CMD ["python3", "preprocess.py", "all"]