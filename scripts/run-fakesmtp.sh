#!/bin/sh

CURRENT_DIR=$(cd $(dirname $0); pwd)

cd $CURRENT_DIR/../docker/

docker-compose -f docker-compose-fakesmtp.yml -p fakesmtp-server up
