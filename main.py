import requests
import json
import time
from datetime import datetime
import csv

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers, params):

    response = requests.request("GET", url, headers=headers, params=params)
    #print(response.status_code)
    #print(response.headers)
    if response.status_code==503:
        print("wait for ",30," seconds")
        time.sleep(30)
        return response.status_code, {}

    if int(response.headers['x-rate-limit-remaining'])>1:
        print(response.headers['x-rate-limit-limit'],response.headers['x-rate-limit-limit'])
        if response.headers['x-rate-limit-limit']=='3000':
            response.headers['x-rate-limit-limit']='300'
        print("wait for ",(15*60/int(response.headers['x-rate-limit-limit']))," seconds")
        time.sleep((15*60/int(response.headers['x-rate-limit-limit'])))
    else:
        print("wait for ",int(response.headers['x-rate-limit-reset'])-time.time()," seconds")
        time.sleep(int(response.headers['x-rate-limit-reset'])-time.time())

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.status_code,response.json()



search_url = "https://api.twitter.com/2/tweets/search/all"
bearer_token='AAAAAAAAAAAAAAAAAAAAAARzMQEAAAAAXMzA%2FfP%2FrhX9rb2Ab4b5b6Gb2tg%3DlJpTXKlZ2uSbTrDOALHZsOsLhMzi8bFGia4K8dgzSqMVw7KvQA'
headers = create_headers(bearer_token)

file_name='dicembre2021.csv'
next_token=None
while next_token!=0:
    query_params = {
            'query': ' (DDL OR zan OR #DDLZan) '
                     ' lang:it '
                     ' -is:retweet ' #no retweets
                     ' -is:reply '   #no replies
                     ' -is:quote '   #no quotes
                     ' -has:links '  #no URLs
                     ' -has:media '  #no media
                     ' -has:images ' #no images
                     ' -has:videos ' #no videos
                     ' -is:nullcast '#no advertising tweets
        ,
        'max_results': 500,
        'next_token' : next_token,
        'start_time':datetime.strftime(datetime(2021,12,1,0,0,0), '%Y-%m-%dT%H:%M:%SZ'),
        'end_time':  datetime.strftime(datetime(2021,12,31,23,59,0),    '%Y-%m-%dT%H:%M:%SZ'),
        'tweet.fields':'author_id,'
                       'created_at,'
                       'public_metrics,'
                       'source',
                        }
    status=0
    while status!=200:
        try:
            status,json_response = connect_to_endpoint(search_url, headers, query_params)
            #print(status)
        except Exception as e:
            print(e)
            print(status)
            time.sleep(30)

    print(json.dumps(json_response['meta']))
    if 'meta' in json_response:
        if 'next_token' in json_response['meta']:
            next_token=json_response['meta']['next_token']
        else:
            next_token=0
    else:
        next_token=0

    if 'data' in json_response:
        #print(len(json_response['data'])," tweets recovered")
        for tweet in json_response['data']:
            #print(tweet['created_at'],tweet['text'],tweet['public_metrics'],)
            file = open(file_name, "a")
            csv_file=csv.writer(file,delimiter=";",quotechar="\"")
            #file.write(json.dumps(tweet)+"\n")
            csv_file.writerow([tweet['id'],tweet['author_id'],tweet['created_at'],tweet['text'],tweet['source'],tweet['public_metrics']])
            file.close()
    else:
        print("Empty result")

