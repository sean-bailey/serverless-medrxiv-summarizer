import json
import os
import sys
import re
sys.path.append(os.environ['EFS_PIP_PATH'])
sys.path.append(os.environ['MNT_DIR'])
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import boto3
MAINDIR="/mrm8488-roberta-med-small2roberta-med-small-finetuned-cnn_daily_mail-summarization/"
BASEDIR=str(os.environ['MNT_DIR'])+MAINDIR
TOKENIZERDIR=BASEDIR+"tokenizer"
MODELDIR=BASEDIR+"model"
CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def getTitle(soup):
    return(soup.find(id="page-title")).text

def getSoup(url):
    medpage=requests.get(url, timeout=10)
    return BeautifulSoup(medpage.content, "html.parser")

def getResultsConclusion(soup):
    strongs=soup.find_all('strong')
    resultsorconclusion=False
    results=""
    conclusion=""
    for strong in strongs:
        if "RESULTS" in strong.text.upper():
            results=strong.parent.text.replace("RESULTS","")
            resultsorconclusion=True
        if "CONCLUSION" in strong.text.upper():
            conclusion=strong.parent.text.replace("RESULTS","")
            resultsorconclusion=True
    if not resultsorconclusion:
        abstractdiv=soup.find("div",id="abstract-1")
        results=abstractdiv.text
    if len(results) < 1:
        results=abstractSearcher(soup)
    if len(results) <1 and len(conclusion) < 1:
        raise ValueError("Could not find an abstract, results or conclusion in the page")
    return results,conclusion

def abstractSearcher(soup):
    absresults=soup.body.findAll(text="Abstract")
    for result in absresults:
        if result.parent.parent.text != "Abstract":
            return result.parent.parent.text
    return ""


#https://github.com/huggingface/transformers/issues/2422
#I need to upload all the models from s3 first
#go into the json configurations downloaded
def testSummarizer(results,conclusion,modeldir=MODELDIR,tokenizerdir=TOKENIZERDIR):
    to_tokenize = results + " " + conclusion
    text=to_tokenize
    tokenizer = AutoTokenizer.from_pretrained(tokenizerdir)

    model = AutoModelForSeq2SeqLM.from_pretrained(modeldir)

    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs=model.generate(
        inputs['input_ids'],max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True
    )

    outputtext=tokenizer.decode(outputs[0])
    outputtext=cleanhtml(outputtext)

    return outputtext

def scrapeAndSummarize(url,modeldir=MODELDIR,tokendir=TOKENIZERDIR):
    soup=getSoup(url)
    title=getTitle(soup)
    results,conclusions=getResultsConclusion(soup)
    summary=testSummarizer(results,conclusions,tokenizerdir=tokendir,modeldir=modeldir)#summarizeResults(results,conclusions)
    fullstring={"title":title,"url":url,"conclusion":summary}

    return fullstring

def mainFunction(event, context):
    body="you need to specify a url."
    try:
        if 'body' in event:
            bodyresponse=None
            if str(type(event['body']))=="<class 'str'>":
                bodyresponse=json.loads(event['body'])
            else:
                bodyresponse=event['body']
            if 'url' in bodyresponse:
                myurl=bodyresponse['url']
                #data=json.loads(event['body'])
                #dirdict=loadToMemory(inputbucket=inputbucket,inputfile=inputfile)
                body=scrapeAndSummarize(myurl)
    except Exception as e:
        print(e)
    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
