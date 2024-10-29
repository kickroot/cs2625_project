from bs4 import BeautifulSoup
import boto3
import json, shutil, os

s3 = boto3.client('s3')

# Constants
local_bucket_folder = "bucket"
bucket_name = 'cs02625-project'

# Function to read HTML file and parse it
def parse_html(file_path):
    # Open and read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        json_content = json.load(file)
        html_content = json_content['text']
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    div_content = soup.find("section", class_="release-body")
    # Find all <p> elements
    div_content = soup.find_all("p")

    # Print each <p> element's content
    content_list = []
    for i, paragraph in enumerate(div_content, start=1):
        content_list.append(paragraph.text)
    content = ''.join(content_list)

    return {
        'keyword': json_content['keyword'],
        'text': content 
    }

# Get all press releases
def list_press_releases(bucket_name):
    # List all objects in the bucket
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

# Delete all populated folders
if os.path.exists(local_bucket_folder):
    shutil.rmtree(local_bucket_folder)

# Ensure the local directory exists
# if not os.path.exists(local_directory):
#     os.makedirs(local_directory)    

for r in list_press_releases(bucket_name):
    names = r.split("/", 1)
    folder = names[0]
    file_name = names[1]
    path = f"{local_bucket_folder}/{folder}"
    if not os.path.exists(path):
        os.makedirs(path)    

    print(f"folder={folder} file={file_name}")




# Path to your HTML file
# file_path = 'test.json'

# # Call the function to parse and find the elements
# print(parse_html(file_path))

