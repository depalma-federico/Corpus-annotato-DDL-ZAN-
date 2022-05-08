import csv
from collections import Counter

thisdict = {}

#with open('esport.csv','r') as file: #va bene anche così, ma non mi piace molto usare with
file = open('esport.csv','r')
reader = csv.DictReader(file)

for row in reader:
    if row['tweet_id'] not in thisdict:
        thisdict[row['tweet_id']] = []
    thisdict[row['tweet_id']].append(row['stance'])
file.close()
print(thisdict)

for key_tweet_id, value_annotationi in thisdict.items():
    c = Counter(value_annotationi)

    for row in thisdict:
        thisdict[key_tweet_id]=c.most_common(1)

print(thisdict)
#così ho modificato il tuo codice per fare quello che ci eravamo detti per mail

"""
qui utilizzo parte del tuo codice per creare
un file con 3 colonne tweet_id, text, gold_label, labels
"""

thisdict={}
file = open('esport.csv','r')
reader = csv.DictReader(file)

for row in reader:
    if row['tweet_id'] not in thisdict:
        thisdict[row['tweet_id']] = {'text': row['text'], 'labels': []}
    thisdict[row['tweet_id']]['labels'].append(row['stance'])

print(thisdict)
file_out=open("gold.csv","w")
file_out_csv=csv.writer(file_out,delimiter=",",quotechar="\"")
for key_tweet_id, value in thisdict.items():
    c = Counter(value['labels'])
    gold='N/D'
    if c.most_common(1)[0][1]>=2:
        gold=c.most_common(1)[0][0]
    file_out_csv.writerow([key_tweet_id,value['text'],gold,[(key, value) for key, value in c.items()]])
file_out.close()
