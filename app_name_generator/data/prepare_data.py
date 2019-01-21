#-*- coding: utf-8 -*- 


import sys
import pandas as pd

input_file = sys.argv[1]

data = pd.read_csv(input_file)
print (data)
exit()
data["App"] = data["App"].apply(lambda s: s.lower())
app_names = data["App"].tolist()
data["App"].to_csv("app_names.csv", encoding="utf-8", index=False)



