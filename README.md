# Task Management System

### Requirement:
* Flask
* MySQL
* Rabbit MQ
* Socket.IO
* Celery
* Swagger

1. git clone https://github.com/sbsanjaybharti/tms.git
2. cd tms
3. docker-compose build
4. docker-compose up --force-recreate
5. Open one more terminal follow this steps on the terminal
### New terminal for task management system 
 1. docker-compose exec task-management-api /bin/bash
 2. python run.py db init
 3. python run.py db migrate
 4. python run.py db upgrade
 5. celery -A app.main.utility.celery.celey worker --loglevel=info
 
 ### Now aplication is ready
 You can follow the video omini-1.mp4 present in repository.
 Also you can find archtecture task_management_system.xml in same repository
 also you can follow by drag and drop to draw.io
 or else click on the link:
 https://www.draw.io/#Hsbsanjaybharti%2Ftms%2Fmaster%2Ftask_management_system.xml
 
 ### URL:
 Application consist of dynamic IP;
 So, localhost:8080 for traefik. Here you can see the list of running service URL(Frontends) and IP(Backends).
  URL will work only with SSL configuration. So follow the IP.
 1. traefik: localhost:8080 
 2. Mysql admin: backend-phpmyadmin IP (username: root, password: example)
 3.Rabbit: backend-rabbit IP (username: rabbitmq, password: rabbitmq)
 4. Rabbit: backend-rabbit IP (username: rabbitmq, password: rabbitmq)
 5. Application frontend: backend-tmapi IP with broadcast/ For example: http://192.168.48.9:9000/broadcast
 6. Application Backend API: backend-tmapi IP with broadcast/ For example: http://192.168.48.9:9000
 