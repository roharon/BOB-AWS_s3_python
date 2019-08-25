import boto3
import datetime
import json

bucket_name = 'roharon-bob-s3'
object_key = 'roharon-bob-s3-result.txt'

with open("./key.json", 'r') as f:
    json_content = json.load(f)
    ACCESS_ID = json_content['ACCESS_ID']
    ACCESS_KEY = json_content['ACCESS_KEY']
    SESSION_TOKEN = json_content['SESSION_TOKEN']

s3client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key=ACCESS_KEY,
    aws_session_token=SESSION_TOKEN
)

print('Creating new bucket with name: {}'.format(bucket_name))
s3client.create_bucket(Bucket=bucket_name)

list_buckets_resp = s3client.list_buckets()
for bucket in list_buckets_resp['Buckets']:
    if bucket['Name'] == bucket_name:
        print('(Just created) --> {} - there since {}'.format(bucket['Name'], bucket['CreationDate']))

print('Uploading some data to {} with key: {}'.format(bucket_name, object_key))


EXPIRES = datetime.datetime.now() + datetime.timedelta(days=9999)
s3client.put_object(Bucket=bucket_name, Key=object_key, Body=b'KITRI BoB 8th!', ACL='public-read', Expires=EXPIRES)
url = s3client.generate_presigned_url('get_object', {'Bucket': bucket_name, 'Key': object_key})

print('\nTry this URL in your browser to download the object:')
print(url)

try:
    input = input()
except NameError:
    pass
input("\nPress enter to continue...")

print('\nNow using Resource API')

s3resource = boto3.resource('s3')
bucket = s3resource.Bucket(bucket_name)
obj = bucket.Object(object_key)

print('Bucket name: {}'.format(bucket.name))
print('Object key: {}'.format(obj.key))
print('Object content length: {}'.format(obj.content_length))
print('Object body: {}'.format(obj.get()['Body'].read()))
print('Object last modified: {}'.format(obj.last_modified))
print('\nDeleting all objects in bucket {}.'.format(bucket_name))
delete_responses = bucket.objects.delete()

for delete_response in delete_responses:
    for deleted in delete_response['Deleted']:
        print('\t Deleted: {}'.format(deleted['Key']))
    print('\nDeleting the bucket.')
    bucket.delete()