#!/bin/sh
docker run --platform linux/amd64 -e GOOGLE_SEARCH_KEY=${GOOGLE_SEARCH_KEY} -e DATE_RESTRICT=y10 -p 8080:8080 lambda-indexer:test