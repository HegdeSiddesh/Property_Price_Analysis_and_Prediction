import requests
import json
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import argparse


'''
Function to return header.
Q. How to get the header? 
A. https://stackoverflow.com/questions/69141055/python-requests-does-not-get-website-that-opens-on-browser
1. Open the link in incognito window with the network tab open.
2. Copy the first request made by right clicking -> copy -> copy as curl
3. Go to https://curlconverter.com/. Paste the curl command to get the equivalent python requests code.
'''
def get_headers():
    headers = headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'Origin': 'https://www.google.com',
    'Alt-Used': 'www.google.com',
    'Connection': 'keep-alive',
    # 'Cookie': 'AEC=Ae3NU9N4JgxpypL_LEgegjJC_3Cyn2Iyfzv9dLYGpW3GX-y-y1fEq1cyKJg; NID=512=LQTGnxwrfr_a_yhhl1qdf_anNAf8nBHVHe_KnWJFby0qiLqExJeb-G-2G-vTQZaAd7kTwTLp9xc8zDjuZelaQzXQfEkw1X4jt062N7LjU_G8paEJ4UkpuZnpOuvE9zm7nVh0C6Cy3t-dAkOhzChqDSy-UWa8Gmy01I6tzCp7g2vTYcuqbya-Sis17JMh9pWTK2r04Uyx7Ik; ANID=AHWqTUnzSu3vozPJ0X4hIQEN8-uUhLxNAepfnG-NpxG0keHbAQTdecm7Imgf3ZO7; 1P_JAR=2024-03-30-15; DV=g6rWBsGPnPoYcNh6fbLcG-jm0aj-6Bg',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    # 'Content-Length': '0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }
  
    return headers


'''
Function to get the details from webpage url.
request.get() may not return properly or may take too much time.
Hence add headers with the url for get request.

NOTE : Threading is for working in parallel, Async is for waiting in parallel
'''
def fetch_page_data(sectors):
    results = {}
    for sec in sectors:
        sector_val = sec
        results[sec] = ""
        sec = sec.replace(' ','+')
        print(sec)
        url = f"https://www.google.com/search?q={sec}+gurgaon+coordinates+latlong"
        page = requests.get(url, headers=get_headers())
        time.sleep(2)
        #<div class="Z0LcW t2b5Cf">28.3971° N, 77.0867° E</div>
        page_content = BeautifulSoup(page.text, 'html.parser')
        tag_1 = page_content.find_all("div", {"class":"Z0LcW t2b5Cf"})
        if len(tag_1) >= 1:
            tag_1 = tag_1[0].text
            results[sector_val] = tag_1
        print(tag_1)
    return results

def merge_results_to_data(data, results):
    data['latitude'] = data['sector'].apply(lambda x:str(results[x]).split(',')[0][:-2])
    data['longitude'] = data['sector'].apply(lambda x:str(results[x]).split(',')[1][:-2])
    data['latitude'] = data['latitude'].astype(float)
    data['longitude'] = data['longitude'].astype(float)
    print(data)
    with open('gurgaon_properties_with_latlong.csv', 'w') as merged_file:
        data.to_csv(merged_file)


if __name__ == "__main__":
    data = pd.read_csv("/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/data/gurgaon_properties_missing_value_imputation.csv")

    parser = argparse.ArgumentParser(description='Latlong scraping script')
    parser.add_argument('--revisit_failures', type = str , default='False', required=False, help ='True if rechecking of failed sectors analysis')
    args = parser.parse_args()
    if args.revisit_failures=='True':
        with open('sector_latlong.json','r') as latlong_res:
            sectors = json.load(latlong_res)
        #print(list(sectors.keys()))
        for sec in sectors.keys():
            #Removing 'degree' sign from coordinates
            if sectors[sec] != '':
                sectors[sec] = str(sectors[sec]).replace('\u00b0','')
        print(sectors)
        sector_list = [sec for sec in list(sectors.keys()) if sectors[sec]=='']
        print(sector_list)
        print(len(sector_list))
        #exit(0)
        result = fetch_page_data(sector_list)
        for sec in result.keys():
            sectors[sec] = result[sec]
        
        merge_results_to_data(data,sectors)
        #exit(0)
        with open('sector_latlong.json','w') as latlong_res:
            json.dump(sectors, latlong_res)
    else:
        sectors = data['sector'].unique()
        result = fetch_page_data(sectors)
        with open('sector_latlong.json','w') as latlong_res:
            json.dump(result, latlong_res)


