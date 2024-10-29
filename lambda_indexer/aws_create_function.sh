#!/bin/sh
aws lambda create-function \
  --function-name lambda-indexer \
  --package-type Image \
  --code ImageUri=134448787187.dkr.ecr.us-east-2.amazonaws.com/cs02625-indexer:latest \
  --role arn:aws:iam::134448787187:role/docdb-owner