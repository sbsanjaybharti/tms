FROM python:3.6.8-jessie
#Copy docker startup script and copy application code.
RUN pip install --upgrade pip
RUN pip install gevent

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
# Copy CODE
COPY . /app
## Default Workdir
WORKDIR /app
#RUN pip3 install awscli --upgrade --user
EXPOSE 8001
#Run docker startup script.
# CMD ["/app/docker-local-entrypoint.sh"]
# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]