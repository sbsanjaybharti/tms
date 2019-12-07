#!/bin/bash

if [[ -z $APP_NAME ]]; then
	echo "Variable APP_NAME not set - Please set this using the -e flag"
    exit 1
else
    cd /app
    yes | python run.py db migrate
    yes | python run.py db upgrade
    uwsgi --http :8001 \
    --http-websockets \
    --processes 2 \
    --threads 2 \
    --wsgi-file /app/wsgi.py
fi