import os
import json
import boto3
import secrets

lexClient = boto3.client('lexv2-runtime')

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

# def createLexResponse(intent):
#     return {
#         'sessionState': {
#             "dialogAction": {
#               "type": "Delegate"
#             },
#             "intent": intent
#         },
#         'messages': [
#             {
#                 'contentType' : 'PlainText',
#                 'content' : 'Next Message from the Lambda Func'
#             }
#         ]
#     }

def genLambdaResponse(keywords):
    return {
        'statusCode': 200,
        'body': json.dumps({"keywords" : keywords}),
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
    return genLambdaResponse(keywords)