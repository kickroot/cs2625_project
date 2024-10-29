import boto3
import os

# Initialize an S3 client
s3 = boto3.client('s3')

# Define the S3 bucket name
bucket_name = 'cs02625-project'

# Define the local directory where files will be saved
# local_directory = 'path/to/local/directory'

# Ensure the local directory exists
# if not os.path.exists(local_directory):
#     os.makedirs(local_directory)

# Function to list and download all files from the bucket
def download_all_files_in_bucket(bucket_name, local_directory):
    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        # Iterate over all files in the bucket
        for obj in response['Contents']:
            print(obj['Key'])
            # file_key = obj['Key']
            # file_name = os.path.basename(file_key)  # Get the file name from the key
            
            # if file_name:  # Ensure it's not an empty folder key
            #     local_file_path = os.path.join(local_directory, file_name)
            #     print(f"Downloading {file_key} to {local_file_path}")
            #     s3.download_file(bucket_name, file_key, local_file_path)

# Main script execution
download_all_files_in_bucket(bucket_name, "")
