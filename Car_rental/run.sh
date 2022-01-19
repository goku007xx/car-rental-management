#!/bin/bash

sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'trial@123'"
sudo -u postgres psql -c "CREATE DATABASE trial_db"
pip3 install Django
pip3 install psycopg2
python3 manage.py makemigrations
python3 manage.py migrate
sudo -u postgres psql -d trial_db -f roles.sql
sudo -u postgres psql -d trial_db -f dml.sql
