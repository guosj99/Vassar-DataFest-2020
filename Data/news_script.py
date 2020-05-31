import pandas as pd
import numpy as np
import os
from eventregistry import *

# Get key at http://eventregistry.org/register
# Look for API key in profile page
myKey = '3791b6b8-3d9e-4f63-bc29-021c57b8b23e'
er = EventRegistry(apiKey = myKey)

user_keywords = input('\nEnter keyword(s) separated by comma (e.g. "coronavirus, trump"): ')
keywords_array = [x.strip() for x in user_keywords.split(',')]

source_default = ["cnn.com", "nytimes.com", "msnbc.com", "foxnews.com", "wsj.com"]

print("\nDefaut: CNN, The New York Times, Fox News, MSNBC, The Wall Street Journal")
user_pol = input('Please enter source url(s) separated by comma (Enter "default" for default sources): ')
source_pol = source_default
if (user_pol != 'default'):
	source_pol = [x.strip() for x in user_pol.split(',')]

print("\nStart: 2020-04-06")
print("Wave 1: 2020-04-14")
print("Wave 2: 2020-04-21")
print("Wave 3: 2020-04-28")
print("Wave 4: 2020-05-05")
print("Wave 5: 2020-05-12")
print("Wave 6: 2020-05-19")
print("End: 2020-05-27")

start_date = input("\nEnter start date (format YYYY-MM-DD): ")
end_date = input("Enter end date (format YYYY-MM-DD): ")
min_sent = input("\nEnter minimum sentiment >= -1.0 (Enter -1 for all news): ")
max_sent = input("Enter maximum sentiment <= 1.0 (Enter 1 for all news): ")

# print(f"keywords_array: {keywords_array}")
# print(f"source_pol: {source_pol}")
# print(f"start_date: {start_date}")
# print(f"end_date: {end_date}")
# print(f"min_sent: {min_sent}")
# print(f"max_sent: {max_sent}")

# create new query object
q = QueryArticlesIter(
        keywords = QueryItems.AND(keywords_array),
        sourceUri = QueryItems.OR(source_pol),
        dateStart = start_date,
        dateEnd = end_date,
        keywordsLoc = "body", # "body" or "title"
        minSentiment = float(min_sent),
        maxSentiment = float(max_sent),
        dataType = "news")

date_array = []
url_array = []
title_array = []
body_array = []
source_array = []
sentiment_array = []

count = 0

q_exec = q.execQuery(er, sortBy = "rel", 
        returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(eventUri = False, authors = False, sentiment = True)),
        maxItems = 999999999)

for article in q_exec:
    count = count + 1
    dict_art = {}

    for k, v in article.items():
        if (k == 'date'):
            date_array.append(v)
        elif (k == 'url'):
            url_array.append(v)
        elif (k == 'title'):
            title_array.append(v)
        elif (k == 'body'):
            body_array.append(v)
        elif (k == 'sentiment'):
            sentiment_array.append(v)
        elif (k == 'source'):
            source_array.append(v['title'])

dict_q = {'date':date_array, 'source':source_array, 'sentiment':sentiment_array, 'title':title_array, 'body':body_array, 'url':url_array}
df_q = pd.DataFrame(dict_q)

print(f"{count} articles found.")

path = os.getcwd()
user_file = input("Enter file name: ")
filename = (f'{user_file}.csv')
df_q.to_csv(filename, index=False)
print(f"Your file {filename} has been saved to {path}.")
