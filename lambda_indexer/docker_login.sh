#!/bin/sh
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 134448787187.dkr.ecr.us-east-2.amazonaws.com
