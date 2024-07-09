# Use the official Python 3 Docker image.
FROM python:3.9-slim

# Copy requirements.txt
COPY requirements.txt ./

# Install VIM and other utilities
RUN apt-get update && apt-get install -y apt-file vim && \
    apt-file update && \
    apt-get install -y tzdata

# Set timezone to Germany (Berlin)
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
ENV TZ="Europe/Berlin"

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Set working directory
WORKDIR /usr/src/app

# Copy project source code
COPY . .

# Run the crawler
CMD [ "python3", "./jobs/main.py" ]