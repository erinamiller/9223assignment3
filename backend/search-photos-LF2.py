import os
import json
import boto3
import secrets
import requests
from requests_aws4auth import AWS4Auth

OS_URL = "https://search-photos2-jcqux6yd5tpcedvcthlule75ga.us-east-1.es.amazonaws.com/photos"
region = 'us-east-1'
service = 'es'

lexClient = boto3.client('lexv2-runtime')
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

BOT_ID = "TPTWJC5A5J"
BOT_ALIAS_ID = "TSTALIASID"

def getKeywordsFromIntent(intent):
    allValues = []
    try:
        allValues = intent['slots']['keyword']['values']
    except:
        allValues = []
    resolvedVals = []
    for val in allValues:
        resolvedVals.append(val['value']['resolvedValues'][0])
    return resolvedVals

def getBestInterp(allInterps):
    bestInterp = {}
    currHighConf = -1
    for interp in allInterps:
        if ("nluConfidence" in interp) and (interp['nluConfidence']['score'] > currHighConf):
            bestInterp = interp
            currHighConf = interp['nluConfidence']
    return bestInterp

def genLambdaResponse(keywords):
    return {
        'statusCode': 200,
        'body': json.dumps({"urls" : keywords}),
        'headers': { 'Access-Control-Allow-Origin': '*'},
    }

def processLexResult(response):
    interps = response['interpretations']
    # print("Received ", len(interps), " interpretations")
    topInterp = getBestInterp(interps)
    keywords = getKeywordsFromIntent(topInterp['intent'])
    print("Got the following keywords,", keywords)
    return keywords

def getQueryString(event):
    return event['queryStringParameters']['q']

def getImageDataFromOS(keywords):
    kwQuery = []
    for kw in keywords:
        kwQuery.append({ "match_phrase": { "labels": kw}})
    query = {
        "query" : {
            "bool" : {
                "should" : kwQuery
            }
        }
    }
    response = requests.post(OS_URL + "/_search", auth=awsauth, data=json.dumps(query), headers={ "Content-Type": "application/json" })
    jsonResp = response.json()
    return jsonResp['hits']['hits']

def getS3Urls(imgDatas):
    urls = []
    for data in imgDatas:
        doc = data['_source']
        urls.append("https://" + doc['bucket'] + ".s3.amazonaws.com/" + doc['objectKey'])
    return urls

def getKeywordsFromLex(str):
    sessionId = secrets.token_urlsafe(16)  
    lexResponse = lexClient.recognize_text(
            botId=BOT_ID,
            botAliasId=BOT_ALIAS_ID,
            localeId='en_US',
            sessionId=sessionId,
            text=str
            )
    return processLexResult(lexResponse)

def lambda_handler(event, context):
    print("Lambda recieved Event", event)
    qstr = getQueryString(event)
    keywords = getKeywordsFromLex(qstr)
    imgData = getImageDataFromOS(keywords)
    s3Urls = getS3Urls(imgData)
    return genLambdaResponse(s3Urls)