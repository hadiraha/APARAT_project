from username_fider_threadpool import user_finder
from profile_parse_threadpool import ProfileFetcher
import os

PROJECT_NAME = 'APARAT1'
MAX_ITR = 100 ## More than 50 will be safe
USER_NAMES_URL = os.path.join(PROJECT_NAME, 'usernames.txt') #Making a path for storing usernames
PAGE_ADDRS_URL = os.path.join(PROJECT_NAME, 'urls.txt')

u = user_finder(PROJECT_NAME, MAX_ITR)
u.multi_fetch()
u.get_username_url()
u.usernames_to_file()
u.usernames_to_database()

p1 = ProfileFetcher(from_db= True)
p1.multi_fetch()
df = p1.df
# print(df)