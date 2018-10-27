#!/bin/bash

./devscripts/delete_db.sh
./devscripts/crea_db.sh

python3 ./manage.py migrate

