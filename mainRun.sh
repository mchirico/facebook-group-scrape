#!/bin/bash
./grabFacebookData.py
./combineData.py
cp _loadFacebook.sql  data
cd data
sqlite3 database.sqlite < _loadFacebook.sql
echo "docker cp <containerId>:/src/data /host/path/target"
echo -e '\n\n'
echo -e "files: /src/data/database.sqlite  /src/data/post.csv"
echo -e "files: /src/data/like.csv  /src/data/msg.csv"



