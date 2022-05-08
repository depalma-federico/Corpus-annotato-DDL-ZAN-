import glob
import csv
import random
from datetime import datetime
import langdetect
import re

def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


########################################################
#parameters
start_date=datetime(2020,10,28)
end_date=datetime(2021,11,12)
sample_size=500
similarity_threshold=0.7 #between 0 and 1
language_threshold=0.7 #between 0 and 1
########################################################

tweets = {}
sample = []

#read all the tweets from all the files
num_files=0
for file_name in glob.glob("data/*.csv"):
    num_files+=1
    file=open(file_name)
    csv_file=csv.reader(file, delimiter=";",quotechar="\"")
    for row in csv_file:
        tweets[row[0]]=row
    file.close()

#filter the tweets
print("recoveder ",len(tweets.keys())," distinct tweets from ",num_files, "files")
tweets=[*tweets.values()]
random.shuffle(tweets)
for tweet in tweets:
    if len(sample)>=sample_size:
        print("escluso soglia")
        continue
    #filter by date
    date= datetime. strptime(tweet[2], '%Y-%m-%dT%H:%M:%S.000Z')
    if not (date >= start_date and date <= end_date):
        #print("escluso data")
        continue
    #filter by source
    if tweet[4] not in ['Twitter for iPad',
                      'Twitter Web App',
                      'Twitter for iPhone',
                      'Twitter Web Client',
                      'Twitter',
                      'Twitter for Mac',
                      'Twitter for Android']:
        print("escluso sorgente")
        continue

    #filter by text token lenght
    if len(tweet[3].split(" "))<5 :
            print("escluso lunghezza")
            continue

    #filter by language
    prediction=langdetect.detect(tweet[3].replace("\n"," "))
    if prediction != 'it':
        print("escluso lingua")
        continue


    #filter if text contains an url
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,tweet[3])
    if len(url)>0:
        print("escluso url")
        continue

    #filter by similarity
    flag=False
    for sampled_tweet in sample:
        if flag:
         continue
        similarity=get_jaccard_sim(tweet[3],sampled_tweet[3])
        if round(similarity,1)>=similarity_threshold:
            flag=True
    if flag:
        print("escluso similarity")
        continue

    #OPZIONALE: pensa ad un filtro che potresti applicare utilizzando retweet_count, reply_count, like_count, quote_count

    sample.append(tweet)

print("final sample of size: ",len(sample))
print("saving sample in a file")
output=open("sample.csv","w")
output_csv=csv.writer(output,delimiter=";",quotechar="\"",quoting=csv.QUOTE_ALL)
for tweet in sample:
    output_csv.writerow(tweet)
output.close()
print("sample saved!")
