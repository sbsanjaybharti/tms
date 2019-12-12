# Task Management System

### Requirement:
* Flask
* MySQL
* Rabbit MQ
* Socket.IO
* Celery

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
 
 