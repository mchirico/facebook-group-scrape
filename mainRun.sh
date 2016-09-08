#!/bin/bash
./grabFacebookData.py
./combineData.py
cp _loadFacebook.sql  data
cd data
sqlite3 database.sqlite < _loadFacebook.sql
cp database.sqlite /tmp/data/.
cp *.csv /tmp/data/.
echo "Files should be in tmp"
echo "docker cp <containerId>:/src/data /host/path/target"
echo -e '\n'
echo -e "files: /src/data/database.sqlite  /src/data/post.csv"
echo -e "files: /src/data/like.csv  /src/data/msg.csv"



