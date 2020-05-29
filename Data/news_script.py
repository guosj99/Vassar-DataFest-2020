import pandas as pd
import numpy as np
import os
from eventregistry import *

# Get key at http://eventregistry.org/register
# Look for API key in profile page
myKey = 'YOUR_API_KEY'
er = EventRegistry(apiKey = myKey)

user_keywords = input('\nEnter keyword(s) separated by comma (e.g. "coronavirus, trump"): ')
keywords_array = [x.strip() for x in user_keywords.split(',')]

mediaLeft = ["cnn.com", "nytimes.com"]
mediaRight = ["foxnews.com", "nypost.com"]
mediaMid = ["bloomberg.com"]

print("\nDefaut: \n Left: CNN, The New York Times \n Right: Fox News, New York Post \n Mid: Bloomberg \n")
user_pol = input('Please enter a political affinity ("left"/"right"/"mid") or url(s) separated by comma: ')
source_pol = []

if (user_pol == 'left'):
	source_pol = mediaLeft
elif (user_pol == 'right'):
	source_pol = mediaRight
elif (user_pol == 'mid'):
	source_pol = mediaMid
else:
	source_pol = [x.strip() for x in user_pol.split(',')]

print("\nWave 1: 2020-04-14")
print("Wave 2: 2020-04-21")
print("Wave 3: 2020-04-28")
print("Wave 4: 2020-05-05")
print("Wave 5: 2020-05-12")
print("Wave 6: 2020-05-19")

start_date = input("\nEnter start date (format YYYY-MM-DD): ")
end_date = input("Enter end date (format YYYY-MM-DD): ")
min_sent = input("\nEnter minimum sentiment >= -1.0 (Enter -1 for all news): ")
max_sent = input("Enter maximum-sentiment <= 1.0 (Enter 1 for all news): ")

# create new query object
q_pos = QueryArticlesIter(
        keywords = QueryItems.AND(keywords_array),
        sourceUri = QueryItems.OR(source_pol), # substitute with any url(s)
        dateStart = start_date,
        dateEnd = end_date,
        keywordsLoc = "body", # "body" or "title"
        minSentiment = float(min_sent),
        maxSentiment = float(max_sent),
        dataType = "news")

date_array = []
url_array = []
title_array = []
source_array = []
sentiment_array = []

pos_count = 0

q_pos_exec = q_pos.execQuery(er, sortBy = "rel", 
        returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(body = False, eventUri = False, authors = False, sentiment = True)),
        maxItems = 999999999) # change @param maxItems to desired integer

for article in q_pos_exec:
    pos_count = pos_count + 1
    dict_art_pos = {}

    for k, v in article.items():
        if (k == 'date'):
            date_array.append(v)
        elif (k == 'url'):
            url_array.append(v)
        elif (k == 'title'):
            title_array.append(v)
        elif (k == 'sentiment'):
            sentiment_array.append(v)
        elif (k == 'source'):
            source_array.append(v['title'])

dict_q_pos = {'date':date_array, 'source':source_array, 'title':title_array, 'sentiment':sentiment_array, 'url':url_array}

df_q_pos = pd.DataFrame(dict_q_pos)

print(f"{pos_count} articles found.")

path = os.getcwd()
user_file = input("Enter file name: ")
filename = (f'{user_file}.csv')
df_q_pos.to_csv(filename, index=False)
print(f"Your file {filename} has been saved to {path}.")
