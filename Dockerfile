FROM ubuntu
MAINTAINER Mike Chirico <mchirico@gmail.com>
RUN apt-get update
RUN apt-get install -y python sqlite3
RUN apt-get install -y python-setuptools python-dev build-essential python-pip
RUN mkdir /src
ADD requirements.txt /src
ADD _loadFacebook.sql /src
ADD grabFacebookData.py /src
ADD combineData.py /src
ADD tokenf.py /src
ADD mainRun.sh /src
ADD LICENSE /src
RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt


