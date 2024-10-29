#!/bin/sh
docker build --platform linux/amd64 -t lambda-indexer:latest .
docker tag lambda-indexer:latest 134448787187.dkr.ecr.us-east-2.amazonaws.com/cs02625-indexer:latest
docker push 134448787187.dkr.ecr.us-east-2.amazonaws.com/cs02625-indexer:latest
