#!/bin/bash
./grabFacebookData.py
./combineData.py
cp _loadFacebook.sql  data
cd data
sqlite3 database.sqlite < _loadFacebook.sql



