FROM ubuntu
MAINTAINER Mike Chirico <mchirico@gmail.com>
RUN apt-get update
RUN apt-get install -y python sqlite3 vim
RUN apt-get install -y python-setuptools python-dev build-essential python-pip

# Yes, do this twice so it get's cached
RUN pip install --upgrade pip
RUN pip install gunicorn==19.6.0
RUN pip install numpy==1.11.1
RUN pip install pandas==0.18.1

RUN mkdir /src
ADD requirements.txt /src
ADD _loadFacebook.sql /src
ADD grabFacebookData.py /src
ADD combineData.py /src
ADD tokenf.py /src
ADD mainRun.sh /src
ADD LICENSE /src
# Someday we'll forget to update the above
RUN pip install -r /src/requirements.txt


