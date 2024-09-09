import requests
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
    with open(add, 'w') as f: # In every itteration of main.py, it will be refreshed to avoid some useless urls and repetitive urls
        pass
    make_file(directory, base_url) # First record in urls.txt is the seed url
    
    while iterations < max_iterations: #just a simple controller when it's supposed to not crawl whol page *** choosing more than 40 would be enough to ensure it's crwaling whole page
        try:
            r = requests.get(valid_url(base_url)) # requst to start point (seed)
            data = r.json()

            if 'links' in data:
                d = data['links']['next'] # Until there is any new page it will achive next page url
            else:
                print("no more links")
                break

            print(f"fetching next url from url:{d} ||\n") # d will indicate the number of iteration of reloading first page
            make_file(directory , d) 
            base_url = d   
            iterations = iterations + 1

        except requests.RequestException as e:
             print(f"An error occurred. This related to next page: {e}")
             break

