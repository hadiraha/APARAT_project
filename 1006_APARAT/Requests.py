import requests
# import pprint
# import json
import os

def valid_url(url):
    return url.replace(r'\/', '/')

def make_dir(adr): # Make dir under adr projrct name
        if not os.path.exists(adr):
            print(f"creating directory {adr}")
            os.makedirs(adr) 

def make_file(address, data):
     make_dir(address) ## Make file in
     filename = os.path.join(address, 'urls.txt')
     with open(filename, 'a') as f:
               f.write(data +'\n')

def url_fndr(base_url, project_name, max_req):
    directory = project_name
    iterations = 0
    max_iterations = max_req
    add = os.path.join(directory , 'urls.txt')
    make_dir(directory)
    with open(add, 'w') as f:
        pass
    make_file(directory, base_url)
    
    # r = requests.get(valid_url(base_url))
    # data = r.json()
    # d = data['links']['next']

    while iterations < max_iterations:
        try:
            r = requests.get(valid_url(base_url))
            data = r.json()

            if 'links' in data:
                d = data['links']['next']
            else:
                print("no more links")
                break

            print(f"fetching next url from url:{d} ||\n")
            make_file(directory , d) 
            base_url = d   
            iterations = iterations + 1

        except requests.RequestException as e:
             print(f"An error occurred: {e}")
             break

# url = 'https://www.aparat.com/api/fa/v1/video/video/list/tagid/1?next=1'
# url_fndr(url, 'test300',200)
