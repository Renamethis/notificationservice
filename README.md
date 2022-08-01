# Notification Service
This web application is a notification web service with a database for collecting statistics and sending notifications. Also, this software uses a task queue to perform periodic message distribution and database management.
# Tech
- Django
- DRF
- drf-yasg(OpenAPI, Swagger, ReDoc)
- django-celery-beat
- Celery
- Redis
- Docker

# Run
To run this web service locally it's necessary to run celery-beat, celery-worker and python Django web-service in three different terminals.
- Celery-beat
```bash
python3 -m celery -A notificationservice beat -l info
```
- Celery-worker
```bash
python3 -m celery -A notificationservice worker -l info
```
- Django web-service
```bash
python3 manage.py runserver
```
# Deploy with Docker
You can deploy with web-application with docker container:
```bash
docker-compose up --build -d
```
Stop containers:
```bash
docker-compose down
```
View logs:
```bash
docker logs --tail {amount of lines} --follow --timestamps {container name}
```
# Testing
To test django unit and functional tests:
```bash
python3 manage.py test -v 2
```
# Usage 

Once the application is running, you can test it by going to http://127.0.0.1:8000/api/ and using DRF for testing. You can also go to http://127.0.0.1:8000/docs/ or http://127.0.0.1:8000/redoc/ for interactive API testing. The OpenAPI specification is available at: http://127.0.0.1:8000/openapi.yaml.
