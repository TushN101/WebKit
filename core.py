from urllib.parse import urlparse
import requests
import threading
import queue
import time
from datetime import datetime
import json

CGREEN = '\033[32m'  
CEND = '\033[0m'  
subdirectories = []

def fail(error):
    print(f"[!] There was an issue with the following script | Error : {error}")
    exit()

def fetch_url():
    # Taking input from the user
    website_url = input("Enter the URL of the website: ").strip()
    
    #Parsing the url for further checking and debugging
    parsed_url = urlparse(website_url)

    #Determining the scheme of the url . only going to deal with http or https
    if parsed_url.scheme == 'http':
        print("[-] The URL is using HTTP")
    elif parsed_url.scheme == 'https':
        print("[-] The URL is using HTTPS")
    else:
        fail("The url doesnt have the scheme http or https")

    #Determing the domain of the url
    domain = parsed_url.netloc
    print(f"[-] Domain is {domain}")

    #Determining the path provided in the url and checking the ends with to add the '/''
    path = parsed_url.path
    if not path.endswith('/'):
    	path = path + "/"
    print(f"[-] Path is {path}")

    #Crafting the final url
    final_url = parsed_url.scheme + "://" + domain + path
    print(f"[-] Final url is {final_url}")

    #Now we are going to validate the final url
    try:
        response = requests.head(final_url,timeout=5)
        if response.status_code in {200}:
            print(f"[-] The website was validated with the code as : {response.status_code}")
            check_cache(final_url)
        else:
            fail("The URL returned with a response code other than needed for validity")
    except Exception as e:
        print(e)

def check_subdirectory(final_url, subdirectory_list, stop_event):
    while not stop_event.is_set():
        try:
            subdirectory = subdirectory_list.get(timeout=1)
            test_url = final_url + subdirectory
            try:
                #print(f"[-] Testing the URL: {test_url}")  # Added for debugging
                response = requests.head(test_url, timeout=5)
                if response.status_code in {200, 301, 302, 204}:
                    print(CGREEN + f"[-] Found a subdirectory: {final_url+subdirectory}" + CEND)
                    subdirectories.append(final_url+subdirectory)
            except requests.RequestException as e:
                pass
                #print(f"[!] Error requesting {test_url}: {e}")
            finally:
                subdirectory_list.task_done()
        except queue.Empty:
            break

def enumerate(final_url):
    # Opens the dictionary file containing common subdirectories
    subdirectory_list = queue.Queue()
    stop_event = threading.Event()

    with open('common.txt', 'r') as file:
        for line in file:
            subdirectory = line.strip()
            if subdirectory:  # Avoid adding empty lines
                subdirectory_list.put(subdirectory)

    threads = []
    
    for i in range(50):
        thread = threading.Thread(target=check_subdirectory, args=(final_url, subdirectory_list, stop_event))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    try:
        # Wait for threads to complete or stop
        while any(thread.is_alive() for thread in threads):
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Operation interrupted by user.")
        stop_event.set()
        for thread in threads:
            thread.join(timeout=2)
        exit()

    update_cache(final_url)

def update_cache(final_url):
    cache_file = 'cache.json'
    current_date = datetime.now().strftime('%Y-%m-%d')

    try:
        with open(cache_file, 'r') as file:
            data = json.load(file)
    except:
        print("[!] Failed to load file")
    
    # Update the cache
    data[final_url] = {
        current_date: {
            'subdirectories': subdirectories
        }
    }

    try:
        with open(cache_file, 'w') as file:
            json.dump(data, file, indent=4)
    except:
        print(f"[!] Error occured saving the file ")

def check_cache(final_url):
    cache_file='cache.json'
    try:
        with open(cache_file ,'r') as file:
            data = json.load(file)

    except:
        print("[!] Failed to load file")

    if final_url in data:
        print(f"[+] {final_url} found in cache.")
        
        # Print the subdirectories found
        for date, info in data[final_url].items():
            print(f"Date: {date}")
            subdirectories = info.get('subdirectories', [])
            if subdirectories:
                print("Subdirectories found:")
                for subdir in subdirectories:
                    print(f"  - {subdir}")
                print("\n\n[-] Now Starting a new Scan")
                enumerate(final_url)
            else:
                enumerate(final_url)

    else:
        print(f"[-] {final_url} not found in cache.")
        enumerate(final_url)


fetch_url()
