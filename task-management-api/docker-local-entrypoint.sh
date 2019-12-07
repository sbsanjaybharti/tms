#!/bin/bash

python run.py db migrate
python run.py db upgrade

if [[ -z $APP_NAME ]]; then
	echo "Variable APP_NAME not set - Please set this using the -e flag"
    exit 1
else

  uwsgi --http :8001 \
  --http-websockets \
  --processes 2 \
  --threads 2 \
  --wsgi-file /app/wsgi.py
#   celery worker -A app.celery --loglevel=info
fi