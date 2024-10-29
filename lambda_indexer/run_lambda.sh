#!/bin/sh
aws lambda invoke --function-name lambda-indexer --payload "fileb://event.json" response.json && cat response.json