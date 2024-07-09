import requests
from pathlib import Path
from Requests import url_fndr

class user_finder:
    base_url = r'https://www.aparat.com/api/fa/v1/user/user/information/username/'
    def __init__(self, file_adress):
        self.file_adress = file_adress
        self.usernames = set()
        self.urls = self.url_reader()
    
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
            user = self.base_url + user
            username_urls.add(user)
        return sorted(username_urls)

def apend_data(dir, data):
    filename = dir + '/usernames.txt'
    with open(filename, 'a') as f:
        f.write(data + '\n')

def set_to_file(dir,data):
    for d in sorted(data):
        apend_data(dir, d)

url = 'https://www.aparat.com/api/fa/v1/video/video/list/tagid/1?next=1'
projname = 'test302'
max_iter = 5
url_fndr(url, projname, max_iter)
urls_file = fr'{projname}' + r'\urls.txt'

u = user_finder(urls_file)
u.fetch_data()
username_urls = u.get_username_url()
print(username_urls)

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