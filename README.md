# todo-list API

## Environment configuration

*Please make sure the following programs are installed in your system

*For Windows users, please make sure to run any applications with GitBash.
>Docker, Docker compose, Python 3, virtualenv, GitBash(Windows only)


### Docker
* For Linux user may need to install docker-compose separately
> https://docs.docker.com/get-docker/
 
### Python 3
* Make sure to install Python3.9
> https://www.python.org/downloads/

### GitBash (Only for Windows users)
> https://git-scm.com/downloads

### virtualenv
* For Unix/Mac users
> python3 -m pip install --user virtualenv

* For Windows users
> py -m pip install --user virtualenv

### Creating a python virtual environment

Switch to `app-api` directory

* For Unix/Mac users
> python3 -m venv env

* For Windows users
> py -m venv env

### Activate python virtual environment

* For Unix/Mac users
* Make sure the directory is `scripts`
> source ./activate-env-unix.sh

* For Windows users
* Make sure the working directory is `scripts`
> source ./activate-env-win.sh

For deactivating the python virtual environment
> deactivate

### Installing require python packages

Install the packages by using the following command
Make sure the directory is `scripts`

* For Unix/Mac users
> ./install-python-packages-unix.sh

* For Windows users
> ./install-python-packages-win.sh

### Create `.env` file and generate Django SECRET_KEY
Make sure the directory is `scripts`


1. Run the following command:
> ./create-env.sh

2. Run the following command to generate Django SECRET_KEY

* Make sure the python virtual environment is activated
> ./generate-secret-key.sh

3. Copy the Django SECRET_KEY

4. Switch to `app-api` directory and past your Django SECRET_KEY on the following line of `.env` file:
> export SECRET_KEY=**YOUR_SECRET_KEY**

---

## Run Postgres docker container
Make sure the directory is `scripts`

Run the following command:
> ./run-postgres.sh

---

## Making migrations and migrate
* Make sure the python virtual environment is activated 
* Make sure to change directory to `app-api`


* Please, synchronizes the database state with the current set of models and migrations by running the following command:
> python manage.py migrate

* If you modified or create any new models, please run the following command:
* _To add migrations to an app that doesn’t have a migrations directory, run `makemigrations` with the app’s name._
> python manage.py makemigrations

## Run Django server
* Make sure the python virtual environment is activated
* Make sure the directory is `scripts`

Run the following command to start the server:
> ./run-server.sh

Server URL
> http://127.0.0.1:8000/api/v1/

---

## Run Fake SMTP server
Make sure the directory is `scripts`

* This program allows receiving emails in development environment

Run the following command:
> ./run-fakesmtp.sh

You may access the client fake SMTP from the following URL:
> http://localhost:60500/

