
# Api_yamdb_final

Project Api_yamdb is a platform for collecting user reviews for titles of different categories. Also users can rate titles and commnet reviews.
[![Workflow](https://github.com/squirrel-whtevr/api_yamdb_wf1/workflows/main/badge.svg)]
## Getting Started

The project will be tested and deployed to your server via Github Actions after you push it to your git repository.

### Prerequisites

To run this project on your server you need to add following [git secrets](https://docs.github.com/en/actions/reference/encrypted-secrets) to your repository:
DOCKER_USER, DOCKER_PASSWORD - username and password of your docker account
HOST, USER, SSH_KEY, PASSPHRASE (optional) - server public ip, username used to connect to server, private id_rsa key and passphrase for id_rsa key (if needed)
TELEGRAM_TO, TELEGRAM_TOKEN - ID of your telegram account and token of your telegram bot (if you wish to recieve message about completed workflow)

There is an example .env file named .env.example. Rename it to .env and change values of variables for work with database if needed.
Also you will need server and CLI to connect to your server via SSH. 

### Installing

After github workflow is complete execute following commands via CLI from home directory on your server

To get into app container
```
docker exec -it api_yamdb_web_1 bash
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
To collect static
```
python manage.py collectstatic
```
The app will be available at your server ip address. For example, you can browse titles at http://XX.XX.XX.XX/api/v1/titles, more api specification can be found at http://XX.XX.XX.XX/redoc

## Built With

* [Django](https://www.djangoproject.com) - The web framework used
* [Postgres](https://www.postgresql.org) - The database system used
* [Docker](https://www.docker.com) - Tool used to containerize and run up application
