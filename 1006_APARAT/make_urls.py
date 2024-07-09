import os

file_path = r'test200\usernames.txt'
export_path = r'test200\profileurl.txt'
base_url = r'https://www.aparat.com/api/fa/v1/user/user/information/username/'
profile_urls = set()

with open(file_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        username = line.strip()
        profile_url = base_url + username
        profile_urls.add(profile_url)

with open(export_path, 'w') as f:
    for url in profile_urls:
        f.write(url + '\n')



