import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from Requests import url_fndr
from Requests import valid_url

def read_existing_data(filename): 
    existing_data = set()
    try:
        with open(filename, 'r') as f:
            for line in f:
                existing_data.add(line.strip())
    except FileNotFoundError:
        pass
    return existing_data

def append_data(filename, data):
    with open(filename, 'a') as f:
        f.write(data + '\n')
        # print(f"writing {data} data")

def set_to_file(dir, data): #for creating username file
    filename = os.path.join(dir, 'usernames.txt')
    existing_data = read_existing_data(filename)
    data_set = set(data)
    new_data = data_set - existing_data  # Subtract existing data to get only new unique data    
    if new_data:  # Only write if there are new unique data to add
        print(f"writing new data:{len(new_data)} in {filename}")
        for d in sorted(new_data):
            
            with open(filename, 'a') as f:
                f.write(d +'\n')
    else:
        print("Alreade there is not NEW DATA")
    return print(f"writing new data:{len(new_data)} in {filename}")

#these three functions make sure we are not requsting repetitive uses and saving new data
###______________________________________________________________________________________________________________

class user_finder: ## It gets PROJECT NAME like "APARAT" and MAX itr
    base_url = r'https://www.aparat.com/api/fa/v1/user/user/information/username/' ##Base URL for making APIs  to retrive profiles info
    seed_url = 'https://www.aparat.com/api/fa/v1/video/video/list/tagid/1?next=1'  ##Seed URL for the first page in HOME
    
    def __init__(self, project_name, max_itr):
        self.project_name = project_name
        self.max_itr = max_itr
        self.usernames = set()
        self.file_adress = self.get_adress()
        self.urls = self.url_reader()
        self.username_urls = self.get_username_url()
        self.username_urls = set()

    def get_adress(self):
        url_fndr(self.seed_url, self.project_name, self.max_itr) #Calling the Request.py to crawl on seed page to get the whole page!!!
        file_adress = os.path.join(self.project_name , 'urls.txt') #Adressing the file contain all urls to start and request them
        return file_adress #Return the url.txt file address to use it then

    def url_reader(self):
        urls = set() #put them in a set to avoid repetitive data
        try:
            with open(self.file_adress , 'r') as f: # reading urls from urls.txt
                for line in f:
                    url = line.strip()
                    if url:
                        urls.add(url)
        except FileNotFoundError:
            print("file doesnt exist please recheck")
        except Exception as e:
            print(f"this error: {e} happened")
        return sorted(urls)

    def multi_fetch(self): #make requsts to urls with at least ten worker to make it quicker ## it will invoke two functions 1-fetcher 2-parser
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = {ex.submit(self.fetch_data, url): url for url in self.urls} 
            for future in as_completed(futures):
                url = futures[future]
                try:
                    data = future.result()
                    if data:
                        self.parse_data(data)
                        print(f"Successfully fetched data from: {url}")
                except Exception as e:
                    print(f"Error: {e} From Fetching {url}")

    def fetch_single(self):
        a = 0
        for url in self.urls:
            try:
                r = requests.get(url)
                d = r.json()
                self.parse_data(d)
                print(f"{a}th {url} is fetched")
                a = a + 1
            except requests.RequestException as e:
                print(f"ERROR raised: {e}")

    def fetch_data(self, url): #making requsts to the urls and get data to pass to parser
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
            print(f"Error: {e} From Fetching {url}")
            return None



    def parse_data(self, data): # parsing json to get usernames in each url in urls.txt
        if 'included' in data:
            list = data['included']
            l = len(list)
            for i in range(l):
                if 'username' in list[i]['attributes']:
                    self.usernames.add(list[i]['attributes']['username'])
                else:
                    break
                
    def get_username(self): #sorting usernames
        return sorted(self.usernames)
    
    def get_username_url(self): #making urls for each user
        username_urls = set()
        for user in self.usernames:
            if user:
                u = self.base_url + user
                self.username_urls.add(u)
            else:
                print("NONE TYPE ERROR")
            # print(f"{u} has been made")
        return sorted(username_urls)
    
    def usernames_to_file(self): #storing them to file to requste them after and fetch the users data
        print(f"is creating files by {self.username_urls} , {self.usernames}")
        set_to_file(self.project_name, self.username_urls)

