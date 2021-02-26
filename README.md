
# Api_yamdb_final

Project Api_yamdb is a platform for collecting user reviews for titles of different categories. Also users can rate titles and commnet reviews.
[![Workflow](https://github.com/squirrel-whtevr/api_yamdb_wf1/workflows/main/badge.svg)]()
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run up this project you will need Docker, you can download it from [here](https://www.docker.com/products/docker-desktop) and follow the [installation instructions](https://docs.docker.com)


### Installing

To start working with project execute following commands via bash from project app. It will start two docker containers with api_yamdb and Postgres.
```
docker-compose up
```
To get into app container - execute following command via new bash window
```
docker exec -it infra_sp2_web_1 bash
```
From there you will be able to create database
```
python manage.py makemigrations
python manage.py migrate
```
To create superuser (you will be asked information required for user registration)
```
python manage.py createsuperuser
```
To apply fixtures 
```
python manage.py loaddata dump.json
```
The app will be available at http://127.0.0.1:8000. For example, you can browse titles at http://127.0.0.1:8000/api/v1/titles

## Built With

* [Django](https://www.djangoproject.com) - The web framework used
* [Postgres](https://www.postgresql.org) - The database system used
* [Docker](https://www.docker.com) - Tool used to containerize and run up application