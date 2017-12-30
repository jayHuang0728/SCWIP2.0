import json
import chardet
import urllib.request
import os
import re
from bs4 import BeautifulSoup
import requests
from pprint import pprint

"""
def get_aqiJson(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")


"""
#抓取AQI的JSON檔
def get_aqiJson(url):
    response = requests.get(url)
    # page = urllib.request.urlopen(url1).read()
    #checker = chardet.detect(page)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def store(url):
    data = get_aqiJson(url)
    with open('AQI.json', 'w') as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))




def main():
    print('>>>AQI_json.py<<<')
    try:
        store('http://opendata.epa.gov.tw/ws/Data/AQFN/?$format=json')
    except KeyboardInterrupt as e:
            print('KeyboardInterrupt: 幹嘛中斷我?')
    finally:
            print('END')

if __name__ == '__main__':
    main()


    