#!/usr/bin/env python
import pandas as pd
import csv
import os

def WriteDictToCSV(csv_file, csv_columns, dict_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    return

# load data from the raw txt into a dict list
dicts_data = []
with open('./freeTop540Info.txt','r') as inf:
    for line in inf:
        dicts_data.append(eval(line))
#print(dicts_data[0]['title'])
# translate txt data into CSV format
# title package_name rating downloads category short_desc description
csv_columns = ['title', 'package_name', 'rating', 'downloads', 'category', 'short_desc', 'description']
currentPath = os.getcwd()
csv_file = currentPath + "/freeTop540Info.csv"
WriteDictToCSV(csv_file, csv_columns, dicts_data)

# load CSV data into pd data frame
#df = pd.read_csv("./freeTop540Info.csv", names=['title', 'package_name', 'rating', 'downloads', 'category', 'short_desc', 'description'])
df = pd.read_csv("./freeTop540Info.csv")
print(df)
print("CSV data shape:", df.shape)

#print(df['package_name'][39])
#print(df['package_name'][38])
#print(df['package_name'][37])
# data cleaning
# remove '+' from 'downloads' to make it numeric
# remove ',' from 'downloads' to make it numeric
df['downloads'] = df['downloads'].apply(lambda x: x.replace('+', '') if '+' in str(x) else x)
df['downloads'] = df['downloads'].apply(lambda x: x.replace(',', '') if ',' in str(x) else x)
df['downloads'] = df['downloads'].apply(lambda x: int(x))
print(df['downloads'])
print(df['description'])

def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

# drop chinese rows
#df = df[not check_contain_chinese(df.description)]
print(df['description'])
