import pandas as pd
import numpy as np
import os
from eventregistry import *

# Get key at http://eventregistry.org/register
# Look for API key in profile page
myKey = '3791b6b8-3d9e-4f63-bc29-021c57b8b23e'
er = EventRegistry(apiKey = myKey)

start_date = input("Enter start date (format YYYY-MM-DD): ")
end_date = input("Enter end date (format YYYY-MM-DD): ")
min_sent = input("Enter minimum sentiment (>= -1.0): ")
max_sent = input("Enter maximum-sentiment (<= 1.0): ")

# create new query object
q_pos = QueryArticlesIter(
        keywords = QueryItems.AND(["reopen", "coronavirus"]), # substitute with any keyword(s)
        sourceUri = QueryItems.OR(["cnn.com", "nytimes.com", "msnbc.com"]), # substitute with any url(s)
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

print(f"Positive sentiment: {pos_count} articles found.")

path = os.getcwd()
filename = input("Enter file name (e.g. data.csv): ")
df_q_pos.to_csv(filename, index=False)
print(f"Your file {filename} has been saved to {path}.")
