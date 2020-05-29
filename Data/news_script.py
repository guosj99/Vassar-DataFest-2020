import pandas as pd
import numpy as np
import os
from eventregistry import *

# Get key at http://eventregistry.org/register
# Look for API key in profile page
myKey = 'YOUR_API_KEY'
er = EventRegistry(apiKey = myKey)

# create new query object
q_pos = QueryArticlesIter(
        keywords = QueryItems.AND(["reopen", "coronavirus"]), # substitute with any keyword(s)
        sourceUri = QueryItems.OR(["cnn.com", "nytimes.com", "msnbc.com"]), # substitute with any url(s)
        dateStart = "2020-05-05", # substitute with any date range(s)
        dateEnd = "2020-05-11",
        keywordsLoc = "body", # "body" or "title"
        minSentiment = 0, # int in [-1,1]
        maxSentiment = 1,
        dataType = "news")

date_array = []
url_array = []
title_array = []
source_array = []
sentiment_array = []

pos_count = 0

q_pos_exec = q_pos.execQuery(er, sortBy = "rel", 
        returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(body = False, eventUri = False, authors = False, sentiment = True)),
        maxItems = 100) # change @param maxItems to desired integer

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

print(f"Positive sentiment: {pos_count} articles found.")

path = os.getcwd()
filename = input("Enter file name (e.g. data.csv): ")
df_q_pos.to_csv(filename, index=False)
print(f"Your file {filename} has been saved to {path}.")
