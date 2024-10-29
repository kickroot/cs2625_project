import boto3
import json, shutil, os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

local_bucket_folder = "bucket"
bucket_name = 'cs02625-project'

s3 = boto3.client('s3')


def list_press_releases(bucket_name) -> list:
    '''Get all press releases, returning a list[object paths]'''
    
    continuation_token = None
    releases = []
    while True:
        list_params = {'Bucket': bucket_name}
        if continuation_token:
            list_params['ContinuationToken'] = continuation_token

        response = s3.list_objects_v2(**list_params)
                
        if 'Contents' in response:
            # Iterate over all files in the bucket
            for obj in response['Contents']:
                releases.append(obj['Key'])
        if response.get('IsTruncated'):  # If True, there are more objects to retrieve
                    continuation_token = response['NextContinuationToken']
        else:
            break  # No more objects to list, break the loop

    return releases

objects = list_press_releases(bucket_name)

# Delete and recreate the storage folder
shutil.rmtree(local_bucket_folder, ignore_errors=True)

for obj in objects:
    paths = obj.split("/", 1)
    folder = paths[0]
    file_name = paths[1]
    obj_folder = f"{local_bucket_folder}/{folder}"
    os.makedirs(obj_folder, exist_ok=True)    
    s3.download_file(bucket_name, obj, f"{obj_folder}/{file_name}")     
    print(f"Downloaded {obj}")
