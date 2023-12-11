import json
import boto3
# from botocore.vendored import requests
import requests
from datetime import *
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'

def getAllCustomLabels(labelStr):
    if labelStr:
        labels = labelStr.split(',')
        labels = [s.strip() for s in labels]
        return labels
    else:
        return []

def lambda_handler(event, context):
    print("Received event = ", event)
    # boto3.set_stream_logger(name='botocore')
    rekog = boto3.client('rekognition')
    s3 = boto3.client('s3')
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        # size = record['s3']['object']['size']
        # use rekognition to get labels
        labels = rekog.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            MaxLabels=20
        )
        print("Got response from Rekog")
        imgAttrs = s3.head_object(
            Bucket=bucket,
            Key=key
            )
        print("imgAttrs = ", imgAttrs)
        customLabels = getAllCustomLabels(imgAttrs['Metadata']['customlabels'])
    # use x-amzmeta-customLabels field??
    
    
    # prepare json obj
    obj = {}
    obj['objectKey'] = key
    obj["bucket"] = bucket
    obj["createdTimestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    obj["labels"] = customLabels
    for label in labels['Labels']:
        obj["labels"].append(label['Name'])

    print("Labels = ", obj["labels"])
    # write json obj to opensearch
    
    url = 'https://search-photos2-jcqux6yd5tpcedvcthlule75ga.us-east-1.es.amazonaws.com/photos/_doc'
    obj = json.dumps(obj)
    print("Obj = ", obj)
    res = requests.post(url, auth=awsauth, data=obj, headers={ "Content-Type": "application/json" })
    print("Response code from ES = ", res.status_code)
    print("Response from ES = ", res.content)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'headers': { 
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*'
        }
    }