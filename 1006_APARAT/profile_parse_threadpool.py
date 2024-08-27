from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from Requests import valid_url
import pandas as pd
from Mysql_connector import Mysqlconnector

class ProfileFetcher: #Responsible for get user data and save it on sql
    counter = 0
    def __init__(self, file):
        self.file = file
        self.urls = self.read_file()
        self.df = pd.DataFrame()

    def read_file(self): #
        urls = set()
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    url = line.strip()
                    if url:
                        urls.add(url)
        except FileNotFoundError:
            print("File doesn't exist!!!")
        except Exception as e:
            print(f"{e} occurred!!!")
        return sorted(urls)

    def multi_fetch(self):
        with ThreadPoolExecutor(max_workers= 10) as ex:
            futures = {ex.submit(self.fetch_data, url): url for url in self.urls}
            a = 0
            b = 0
            for future in as_completed(futures):
                url = futures[future]
                try:
                    data = future.result()
                    if data:
                        b += 1
                        print(f"this is {b}th")
                        # self.parse_data_to_df(data)
                        if self.pars_data_to_sql(data):
                            print(f"Successfully fetched data from: {url}")
                            a += 1
                            self.counter += 1
                            print(f"{a} ________________ {self.counter}")
                except Exception as e:
                    print(f"Error: {e} From Fetching {url}")
        return self.show_counter()

    def fetch_single(self):
        a = 0
        for url in self.urls:
            try:
                r = requests.get(valid_url(url))
                data = r.json()
                self.parse_data_to_df(data)
                self.pars_data_to_sql(data)
                print (f"{a}th profile is fetching with this: {url}")
                a = a+1
            except requests.RequestException as e:
                print(f"{a}th raises this error {e}")
 
    def fetch_data(self, url):
        try:
            print(f"Fetching data from: {url}")
            r = requests.get(valid_url(url))
            r.raise_for_status()
            if r.text.strip():
                return r.json()
            else:
                print(f"Received empty response for URL: {url}")
                return None
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None
        
    def pars_data_to_sql(self, data):
        if 'data' in data and 'attributes' in data['data']:
            dic_profile = data['data']['attributes']
            tablename = 'fetched'
            c = Mysqlconnector()
            c.create_table(tablename, dic_profile)
            state = c.insert_value(tablename, dic_profile)
            c.close_connection()
            return state
        return False
            

    def parse_data_to_df(self, data):
        if 'data' in data and 'attributes' in data['data']:
            dic_profile = data['data']['attributes']
            temp_df = pd.DataFrame([dic_profile])
            self.df = pd.concat([self.df, temp_df], ignore_index=True)

    def show_counter(self):
        print(f"{self.counter} is the total number of affected rows in DB")
