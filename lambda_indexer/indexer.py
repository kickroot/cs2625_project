#
# Jason Nichols
# CSE 02625
# HW 1 + Final Project Work
#
import boto3, json, requests
from botocore.exceptions import ClientError

bucket_name = "cs02625-project"
s3 = boto3.client('s3')

# Used to generate some entropy for the google queries by using
# random time periods.
def random_period():
    import random
    prefixes = [("d", 30), ("m", 12), ("y", 10)]    
    period = prefixes[random.randint(0, len(prefixes)-1)]
    return f"{period[0]}{random.randint(1, period[1])}"
random_period()

def object_exists(bucket_name, object_key):
    try:
        # Attempt to retrieve the object's metadata
        s3.head_object(Bucket=bucket_name, Key=object_key)
        print(f"Object '{object_key}' found in '{bucket_name}'.")
        return True
    except ClientError as e:
        # Check if the error is due to the object not existing
        if e.response['Error']['Code'] == '404':
            print(f"Object '{object_key}' not found in '{bucket_name}'.")
            return False
        else:
            # Handle other possible errors
            raise e

#
# Returns a tuple indicating success (True, text), or
# (False, None) in the case of an error
#
def pull_text(url):
    response = requests.get(url)
    if response.status_code != 200:
        return (False, None, response.status_code)
    return (True, response.text, None)

def push_to_s3(bucket_name, keyword, file_id, data):
    data = json.dumps(data, indent=2)
    print(f"Uploading {bucket_name}/{keyword}/{file_id}")
    s3.put_object(Bucket=bucket_name, Key=f"{keyword}/{file_id}", Body=data)
    
#
# This function is called as part of the AWS Lambda serverless runtime.  At the moment the function instantiates a 
# Google Custom Search Engine (using the env variable value stored in GOOGLE_SEARCH_KEY).
#
# Search terms and date restriction are pulled from the event object, which is passed as a JSON blob to the Lambda
# runtime. See both event.json and response.json for the input and outputs, respectively.
#
def handler(event, context):
    import os, logging, hashlib
    from googleapiclient.discovery import build
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print("Running v3")
    print(f"Raw event: {event}")
    logging.info("Event info: %s", event)
    date_restrict=event.get('dateRestrict', random_period())
    print(f"Using dateRestrict={date_restrict}")
    keyword = event['exactTerms']
    search_service = build("customsearch", "v1", developerKey=os.getenv('GOOGLE_SEARCH_KEY'))

    return_payload = []
    start_index = 1
    while start_index <= 91:

        res = search_service.cse().list(cx="d5a71a4f0bfc840a3", exactTerms=keyword, dateRestrict=date_restrict, start=start_index, lr="lang_en").execute()

        for item in res["items"]:
            url = item['link']
            id = hashlib.sha256(url.encode('utf-8')).hexdigest()
            if object_exists(bucket_name, f"{keyword}/{id}"):
                print(f"Object {keyword}/{id} already exists, ignoring")
            else: 
                (success, text, error_code) = pull_text(url)
                if success:            
                    data = {
                        'keyword' : keyword,
                        'url' : url,
                        'title' : item['title'],
                        'text' : text
                    }            
                    push_to_s3(bucket_name, keyword, id, data)                    
                else:
                    print(f"Error fetching URL {url}, request returned {error_code}")
            return_payload.append((item['title'], item['link']))
        start_index = start_index + 10
    return return_payload
