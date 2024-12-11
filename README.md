# ~~Needles~~ Buckets in a Haystack
Rowan University

CS 026205 - Data Quality and Web/Text Mining

## S3 Bucket Name Analysis and Generation

### Repository Guide

> **bucket_analysis/**

Python notebook for EDA w/outputs

> **bucket_downloader/**

Downloads the stored press releases from a private S3 bucket and saves them locally.

> **bucket_indexer/**

Grayhat Warfare API client script that downloads all known public bucket names.  Stores these in a local JSON file.  Requires an API key.

> **html_parser/**

Earlier version of the `bucket_downloader`, unused but saved for posterity.

> **lambda_indexer/**

S3 Lambda function (and Docker image) that executes as a CRON job in the S3 Lambda environment.  This script performs a Google search on prnewswire.com for a given term and iterates through all results, storing the fetched content in an S3 bucket for use in TF-IDF and NER extraction.