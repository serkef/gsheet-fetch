#!/bin/bash

git pull
BUILD_TAG=$(git rev-parse HEAD)
docker build -t gsheet-fetch:${BUILD_TAG} .
docker stop gsheet-fetch
docker rm gsheet-fetch
docker run -d --env-file=.env --restart always --name gsheet-fetch gsheet-fetch:${BUILD_TAG}
