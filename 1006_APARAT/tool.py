usernames = ('1' , 'asd', '34ad', 'qwe')
username_urls = set()
users_data = []

for user in usernames:
    if user:
        u = user
        username_urls.add(u)
        # Creatind dict of usernames and coresponding user urls
        user_data = {
            'id': None,
            'username': user,
            'username_url': u,
            'last_seen': 0
        }
        users_data.append(user_data)
    else:
        print("NONE TYPE ERROR")
    
username_urls = sorted(username_urls)
a = set()
l = len(users_data)
for i in range(l):
    a.add(users_data[i]['username'])
print(a)


    