#!/bin/sh

CURRENT_DIR=$(cd $(dirname $0); pwd)

cd $CURRENT_DIR/../app-api/

python manage.py runserver
