#!/bin/bash

./devscripts/delete_db.sh
./devscripts/crea_db.sh

python3 ./manage.py migrate

python3 ./parser.py
python3 ./student_data.py

