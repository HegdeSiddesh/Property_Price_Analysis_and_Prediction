import requests
import json
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def get_config(cfg_file):
    with open(cfg_file) as config_file:
        config = json.load(config_file)
        return config

'''
Function to return header.
Q. How to get the header? 
A. https://stackoverflow.com/questions/69141055/python-requests-does-not-get-website-that-opens-on-browser
1. Open the link in incognito window with the network tab open.
2. Copy the first request made by right clicking -> copy -> copy as curl
3. Go to https://curlconverter.com/. Paste the curl command to get the equivalent python requests code.
'''
def get_headers():
    headers = {
    'Accept': 'application/x-clarity-gzip',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.99acres.com',
    'Referer': 'https://www.99acres.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Content-Type': 'application/x-www-form-urlencoded',}    
    
    #saved in config.json
    return headers

def get_headers_listing():
    headers_listing =  {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Accept': 'image/avif,image/webp,*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.99acres.com/',
    'Connection': 'keep-alive',
    # 'Cookie': 'MUID=091A48923EF360551A695CA73F68611A; MR=0; SRM_B=091A48923EF360551A695CA73F68611A; MSPTC=oWvI5wB2S2B__lTKIkkyC3PWHg0Mv6JgMV8FU7RHjR4',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

    return headers_listing

'''
Function to get the details from webpage url.
request.get() may not return properly or may take too much time.
Hence add headers with the url for get request.

NOTE : Threading is for working in parallel, Async is for waiting in parallel
'''
def fetch_page_data(page_num):

    config = get_config('config.json')
    url = config['url']
    header = config['headers']
    city = config['city']
    page = requests.get(url.format(city,page_num), headers = header)
    time.sleep(2)
    page_content = BeautifulSoup(page.text, 'html.parser')
    #print(page_content)
    #print(url.format(city,page_num))
    tag_1 = page_content.find_all('script')[0]
    list_elements = json.loads(tag_1.string)['itemListElement']
    #Store the apartment name and the apartment-link mapping in here
    
    #print(type(list_elements[0][0]))
    for apat_entry in list_elements[0]:
        #apat_entry is the dict with flat basic details
        if apat_entry['name'] not in apartments:
            apartments.append(apat_entry['name'])
            links[apat_entry['name']] = []
            links[apat_entry['name']].append(apat_entry['url'])
        else:
            links[apat_entry['name']].append(apat_entry['url'])
        
    #print(links)
    print(len(links))


def parse_apartment_data(url):

    config = get_config('config.json')
    header = get_headers_listing() #config['headers']
    with open("sample_inner.html",'r') as webpage:
        page = requests.get(url, headers = header)
        #print(page.text)
        time.sleep(2)
        page_content = BeautifulSoup(page.text, 'html.parser')
        #print(page_content)
        #print(url.format(city,page_num))

        listing_data = {}
        try:
            listing_data["bathroom"] = page_content.find('span', id = 'bathroomNum').text
        except:
            listing_data["bathroom"] = ''
        try:
            listing_data["bedroom"] = page_content.find('span', id = 'bedRoomNum').text
        except:
            listing_data["bedroom"] = ''
        nearbyLocations_tags = page_content.find_all('span', {"class" : "NearByLocation__infoText"})
        nearbyLocations = []
        listing_data['Hospital'] = 0
        listing_data['Bank'] = 0
        listing_data['Education'] = 0
        listing_data['Religion'] = 0
        listing_data['Transport'] = 0
        #IMP : bank, hospital, school, station, airport, bus, clinic, church, atm, mosque, temple, nursing home, petrol, oil, college, university, doctor
        #Categories = [Bank, Hospital, Education, Transport, Religion]
        for near in nearbyLocations_tags:
            nearby_text = near.text
            if 'hospital' in nearby_text or 'Hospital' in nearby_text or 'clinic' in nearby_text or 'Clinic' in nearby_text or 'Doctor' in nearby_text or 'doctor' in nearby_text:
                listing_data['Hospital'] += 1
                continue
            if 'Bank' in nearby_text or 'ATM' in nearby_text or 'bank' in nearby_text or 'atm' in nearby_text or 'Atm' in nearby_text:
                listing_data['Bank'] += 1
                continue
            if 'School' in nearby_text or 'school' in nearby_text or 'college' in nearby_text or 'College' in nearby_text or 'University' in nearby_text or 'university' in nearby_text:
                listing_data['Education'] += 1
                continue
            if 'Bus' in nearby_text or 'bus' in nearby_text or 'station' in nearby_text or 'Station' in nearby_text or 'Airport' in nearby_text or 'airport' in nearby_text:
                listing_data['Transport'] += 1
                continue
            if 'Mosque' in nearby_text or 'Church' in nearby_text or 'Temple' in nearby_text or 'mosque' in nearby_text or 'church' in nearby_text or 'temple' in nearby_text:
                listing_data['Religion'] += 1
                continue
            #nearbyLocations.append(near.text)
        try:
            listing_data["builtupArea"] = page_content.find('span', id = 'builtupArea_span').text
        except:
            listing_data["builtupArea"] = ''
        try:
            listing_data["carpetArea"] = page_content.find('span', id = 'carpetArea_span').text
        except:
            listing_data["carpetArea"] = ''
        try:
            listing_data["builtupAreaLabel"] = page_content.find('span', id = 'builtupAreaLabel').text
        except:
            listing_data["builtupAreaLabel"] = ''
        try:
            listing_data["balcony"] = page_content.find('span', id = 'balconyNum').text
        except:
            listing_data["balcony"] = ''
        try:
            listing_data["price"] = page_content.find('span', id = 'pdPrice2').text
        except:
            listing_data["price"] = ''
        try:
            listing_data["floor"] = page_content.find('span', id = 'floorNumLabel').text
        except:
            listing_data["floor"] = ''
        try:
            listing_data["facing"] = page_content.find('span', id = 'facingLabel').text
        except:
            listing_data["facing"] = ''
        try:
            listing_data["overlooking"] = page_content.find('span', id = 'overlooking').text
        except:
            listing_data["overlooking"]  = ''
        try:
            listing_data["age"] = page_content.find('span', id = 'agePossessionLbl').text
        except:
            listing_data["age"] = ''
        try:
            listing_data["parking"] = page_content.find('span', id = 'Reserved_Parking_Label').text
        except:
            listing_data["parking"]  = ''   
        try:
            listing_data["furnishing"] = page_content.find('span', id = 'Furnish_Label').text
        except:
            listing_data["furnishing"] = ''
        try:
            listing_data["gated"] = page_content.find('span', id = 'Gated_community').text
        except:
            listing_data["gated"] = ''
        try:
            listing_data["wheelchair"] = page_content.find('span', id = 'WheelChairFriendly').text
        except:
            listing_data["wheelchair"] = ''
        try:
            listing_data["pets"] = page_content.find('span', id = 'PetFriendly').text
        except:
            listing_data["pets"] = ''
        try:
            listing_data["water"] = page_content.find('span', id = 'Watersource_Label').text
        except:
            listing_data["water"] = ''
        try:
            listing_data["power"] = page_content.find('span', id = 'Powerbackup_Label').text
        except:
            listing_data["power"] = ''
        try:
            listing_data["transaction"] = page_content.find('span', id = 'Transact_Type_Label').text
        except:
            listing_data["transaction"] = ''
        
        
        print(listing_data)
        return listing_data

'''
Sequential requests time = 24.541609525680542 seconds
'''
def execute_sequential(config):
    start_time = time.time()
    for i in range(1, config['max_page']):
        fetch_page_data(i)

    end_time = time.time()

    print("Sequential requests time = {} seconds".format(end_time-start_time))
    

'''
Parallel thread requests time = 4.889770746231079 seconds for 25 pages
'''
def execute_parallel(config):

    start_time = time.time()

    with ThreadPoolExecutor() as exec:
        exec.map(fetch_page_data, range(101, 150))

    end_time = time.time()
    print("Parallel thread requests time = {} seconds".format(end_time-start_time))



def execute_parallel(function, parameters, config):

    start_time = time.time()

    with ThreadPoolExecutor() as exec:
        exec.map(function, parameters)

    end_time = time.time()
    print("Parallel thread requests time = {} seconds".format(end_time-start_time))



def get_data_kv_pairs():

    config = get_config('config.json')
    #header = config['headers'] #get_headers()
    #city = config['city'] #'mumbai'

    #links = {}
    #apartments = []
    #execute_sequential(config)

    execute_parallel(config)

    with open("apartment_list.txt", 'a') as apartment_file:
        for apartment in apartments:
            apartment_file.write("\n"+apartment)
        apartment_file.close()

    with open("apartment_links.json", 'a') as links_file:
        #json.dumps(links, links_file, ensure_ascii=False)
        json.dump(links, links_file)
        links_file.close()

def get_apartment_data_from_kv():
    with open("apartment_links.json") as kv_list_file:
        apartments_list = json.load(kv_list_file)

        #Goal : Create a list of Json objects, each for the individual links/listings

        apartment_data = []
        counter = 20
        for k in apartments_list.keys():
            #if counter==0:
            #    break
            #counter -= 1
            entries = apartments_list[k]
            for entry in entries:
                current_data = {"name" : k}
                current_data["url"] = entry
                current_data.update(parse_apartment_data(entry))

                apartment_data.append(current_data)

        #All entries are processed, export the dataframe to excel to be used as dataset
        dfItem = pd.DataFrame.from_records(apartment_data)
        dfItem.to_excel('apartment_dataset.xlsx')




links = {}
apartments = []

if __name__ == "__main__":
    #get_data_kv_pairs()
    get_apartment_data_from_kv()
    #parse_apartment_data("https://www.99acres.com/1-bhk-bedroom-apartment-flat-for-sale-in-dadar-east-south-mumbai-450-sq-ft-spid-F73505173")