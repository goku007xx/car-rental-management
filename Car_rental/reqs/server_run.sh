#!/bin/bash

/etc/init.d/postgresql start
python3 manage.py runserver 0.0.0.0:8000