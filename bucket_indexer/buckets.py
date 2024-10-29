import json, requests, os

start = 0
limit = 1000
results = 1000

headers = {
    'Authorization': f"Bearer {os.getenv('GRAYHAT_API_KEY')}"
}

file = open('buckets.json', 'a')

try:
    while start < results:
        endpoint = f"https://buckets.grayhatwarfare.com/api/v2/buckets?type=aws&start={start}&limit={limit}"
        res = requests.get(endpoint, headers=headers).json()
        results = res['meta']['results']
        for bucket in res['buckets']:
            json.dump(bucket, file, indent=2)
            file.write(',\n')
            print(f"writing {json.dumps(bucket, indent=2)}\n")
        start = start + 1000
finally:
    file.flush()
    file.close()    



