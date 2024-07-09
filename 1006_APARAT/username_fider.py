import requests
import os
# from pathlib import Path
from Requests import url_fndr

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
    
    def fetch_data(self):
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

projname = 'test304'
u = user_finder(projname, 100)
u.fetch_data()
u.get_username_url()
u.usernames_to_file()




# def apend_data(dir, data):
#     filename = dir + '/usernames.txt'
#     with open(filename, 'a') as f:
#         f.write(data + '\n')

# def set_to_file(dir,data):
#     for d in sorted(data):
#         apend_data(dir, d)


# url = 'https://www.aparat.com/api/fa/v1/video/video/list/tagid/1?next=1'
# projname = 'test302'
# max_iter = 5
# url_fndr(url, projname, max_iter)
# urls_file = fr'{projname}' + r'\urls.txt'

# u = user_finder(urls_file)
# u.fetch_data()
# username_urls = u.get_username_url()
# print(username_urls)

# urls_file = r'test300\urls.txt'
# u = user_finder(urls_file)
# u.fetch_data()

# file = r'test200\urls.txt'
# directory = r'test200'
# uset1 = user_finder(file)
# uset1.fetch_data()
# usernames = uset1.get_username()
# print(usernames)
# set_to_file(directory, usernames)




# def user_finder(file_text):
#     urls = set()
#     j = set()
#     try:
#         with open(file_text, 'r') as f:
#             for line in f:
#                 url = line.strip()
#                 if url:
#                     urls.add(url)
#     except FileNotFoundError:
#         print("file doesnt exist please recheck")
#     except Exception as e:
#         print(f"this error: {e} happened")
    
#     for u in urls:
#         try:
#             r = requests.get(u)
#             d = r.json()
#             list = d['included']
#             l = len(list)
#             for i in range(l):
#                 if 'username' in list[i]['attributes']:
#                     j.add(list[i]['attributes']['username'])
#                 else:
#                     break

#         except requests.RequestException as e:
#             print(f"ERROR: {e} is raised")
#     return print(j)

# user_finder(r'E:\Codes\VsCodes\1005_APARAT\test15\urls.txt')

# # url = 'https://www.aparat.com/api/fa/v1/video/video/list/tagid/1?page=2'
# # user_finder(url)