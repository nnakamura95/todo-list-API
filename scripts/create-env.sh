#!/bin/sh

CURRENT_DIR=$(cd $(dirname $0); pwd)

cd $CURRENT_DIR/../app-api/

printf 'export SECRET_KEY= \nexport DEBUG=True' > .env
