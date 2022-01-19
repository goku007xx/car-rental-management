#!/bin/bash

sudo apt install libpq-dev
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'trial@123'"
sudo -u postgres psql -c "CREATE DATABASE trial_db"
sudo -u postgres psql -d trial_db -f roles.sql
sudo -u postgres psql -d trial_db -f dml.sql
