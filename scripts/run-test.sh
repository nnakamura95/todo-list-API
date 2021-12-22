#!/bin/sh

CURRENT_DIR=$(cd $(dirname $0); pwd)

cd $CURRENT_DIR/../app-api/

coverage run --omit='*/env/*' manage.py test
