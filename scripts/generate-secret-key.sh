#!/bin/sh

CURRENT_DIR=$(cd $(dirname $0); pwd)

cd $CURRENT_DIR/../app-api/

python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
