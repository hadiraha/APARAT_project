import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# from pathlib import Path
from Requests import url_fndr
from Requests import valid_url
# url = 'https://www.aparat.com/api/fa/v1/video/video/list/tagid/1?next=1'
# projname = 'test302'
# max_iter = 5
# url_fndr(url, projname, max_iter)
# urls_file = fr'{projname}' + r'\urls.txt'

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

def set_to_file(dir, data):
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

class user_finder:
    base_url = r'https://www.aparat.com/api/fa/v1/user/user/information/username/'
    seed_url = 'https://www.aparat.com/api/fa/v1/video/video/list/tagid/1?next=1'
    
    def __init__(self, project_name, max_itr):
        self.project_name = project_name
        self.max_itr = max_itr
        self.usernames = set()
        self.file_adress = self.get_adress()
        self.urls = self.url_reader()
        self.username_urls = self.get_username_url()
        self.username_urls = set()

    def get_adress(self):
        url_fndr(self.seed_url, self.project_name, self.max_itr)
        file_adress = fr'{self.project_name}' + r'\urls.txt'
        return file_adress

    def url_reader(self):
        urls = set()
        try:
            with open(self.file_adress , 'r') as f:
                for line in f:
                    url = line.strip()
                    if url:
                        urls.add(url)
        except FileNotFoundError:
            print("file doesnt exist please recheck")
        except Exception as e:
            print(f"this error: {e} happened")
        return sorted(urls)

    def multi_fetch(self):
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
            print(f"Error: {e} From Fetching {url}")
            return None



    def parse_data(self, data):
        if 'included' in data:
            list = data['included']
            l = len(list)
            for i in range(l):
                if 'username' in list[i]['attributes']:
                    self.usernames.add(list[i]['attributes']['username'])
                else:
                    break
                
    def get_username(self):
        return sorted(self.usernames)
    
    def get_username_url(self):
        username_urls = set()
        for user in self.usernames:
            u = self.base_url + user
            self.username_urls.add(u)
            # print(f"{u} has been made")
        return sorted(username_urls)
    
    def usernames_to_file(self):
        # print(f"is creating files by {self.username_urls} , {self.usernames}")
        set_to_file(self.project_name, self.username_urls)

# projname = 'test304threadpool'
# u = user_finder(projname, 100)
# u.multi_fetch()
# u.get_username_url()
# u.usernames_to_file()

