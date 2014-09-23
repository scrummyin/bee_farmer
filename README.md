# Bee Farmer

A web based management tool for zookeeper.

## Install

To install clone the repo into a directory. Install the requirements in the requirements.txt file. Set the environment variable ZOOKEEPER_HOSTS to your zookeeper server. Start a uwsgi server and point traffic to it. Bee farmer is a django project, so you can look to https://www.djangoproject.com/ for help.

## Install Example

This is not the recommend way to run this application, but if you need to get it up and running quickly these lines will get the server running against and will point to localhost as the zookeeper server:

    git clone https://github.com/scrummyin/bee_farmer.git
    pip install -r requirements.txt
    export ZOOKEEPER_HOSTS=localhost
    python manage.py runserver 0.0.0.0:8000
