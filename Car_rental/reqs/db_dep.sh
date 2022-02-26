#!/bin/bash

/etc/init.d/postgresql start
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'trial@123'"
sudo -u postgres psql -c "CREATE DATABASE trial_db"
python3 manage.py makemigrations
python3 manage.py migrate
sudo -u postgres psql -d trial_db -f reqs/roles.sql
sudo -u postgres psql -d trial_db -f reqs/dml.sql

