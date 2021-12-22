#!/bin/sh

CURRENT_DIR=$(cd $(dirname $0); pwd)

cd $CURRENT_DIR/../app-api/

py -m pip install -r requirements.txt
