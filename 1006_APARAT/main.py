from username_fider_threadpool import user_finder
from profile_parse_threadpool import ProfileFetcher
import os

PROJECT_NAME = 'APARAT1'
MAX_ITR = 100
USER_NAMES_URL = os.path.join(PROJECT_NAME, 'usernames.txt')

u = user_finder(PROJECT_NAME, MAX_ITR)
u.multi_fetch()
u.get_username_url()
u.usernames_to_file()

p1 = ProfileFetcher(USER_NAMES_URL)
p1.multi_fetch()
df = p1.df
# print(df)