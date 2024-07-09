import requests
import pprint
import json
import os
from Requests import valid_url
from username_fider import url_fndr
from username_fider import user_finder
import pandas as pd



# url = 'https://www.aparat.com/api/fa/v1/user/user/information/username/Royayousefi.ir'
# r = requests.get(valid_url(url))
# data = r.json()
# print(data.keys())
# dic_data = data['data']
# print(dic_data.keys())
# dic_attr = dic_data['attributes']
# pprint.pprint(dic_attr)
# df1 = pd.DataFrame(dic_attr, index= ['1'])
# print(df1)

class profile_fetcher:
    def __init__(self, file):
        self.file = file
        self.urls = self.read_file()
        self.df = pd.DataFrame()
    
    def read_file(self):
        urls = set()
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    url = line.strip()
                    if url:
                        urls.add(url)
        except FileNotFoundError:
            print("File doesnt exict!!!")
        except Exception as e:
            print(f"{e} ocoured!!!")
        return sorted(urls)
    
    def fetch_data(self):
        a = 0
        for url in self.urls:
            try:
                r = requests.get(valid_url(url))
                data = r.json()
                self.pars_data_to_df(data)
                self.pars_data_to_sql(data)
                print (f"{a}th profile is fetching with this: {url}")
                a = a+1
            except requests.RequestException as e:
                print(f"{a}th raises this error {e}")
    
    def pars_data_to_sql(self, data):
        pass

    
    def pars_data_to_df(self, data):
        if 'data' in data and 'attributes' in data['data']:
            dic_profile = data['data']['attributes']
            temp_df = pd.DataFrame([dic_profile])
            self.df = pd.concat([self.df, temp_df], ignore_index= True)


file_path = r'test200\profileurl.txt'
p = profile_fetcher(file_path)
p.fetch_data()

df = p.df
print(df)
# df.to_csv('profiles.csv', index=False)

# with open(file_path, 'r') as f:
#     lines = f.readlines()
#     itr = 0
#     df = []
#     for line in lines:
#         try:
#             r = requests.get(valid_url(line))
#             data = r.json()
#             if 'data' in data:
#                 data_dic = data['data']
#                 if 'attributes' in data_dic:
#                     attr_dic = data_dic['attributes']
#                     pd = pd.DataFrame(attr_dic, index=[itr])
#                     itr = itr + 1
#                 else:
#                     break
#             else:
#                 break
#         except requests.RequestException as e:
#             print(f"this {e} is happened")

