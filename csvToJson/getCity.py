import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import chardet
import json

# 取得頁面
def get_html_code(url):
    # 沒有做異常
    url1 = urllib.request.Request(url)
    page = urllib.request.urlopen(url1).read()
    print('Get Page ({0})'.format(url))
    checker = chardet.detect(page)
    page = page.decode(checker['encoding'])
    return page

# 取得各city的區和鄉鎮的postal code
def get_area(url, cityList):
    for city in cityList:
        # print(url + '/' + quote(city['city']))
        page = get_html_code(url + '/' + quote(city['city']))
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('table', id='zip-table2')
        for item in table.find_all('tr'):
            city['areas'].append({'area_name': item.find('a').get_text(), 'postal_code': item.find('td', 'zip-zip').get_text()})
            # print(item.find('td', 'zip-zip').get_text())
    write_json(cityList, 'city.json')

# 寫json文件
def write_json(data, json_file):
    # 沒有做異常
    with open(json_file, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))

# 取city頁面網址(進入點)
def get_href():
    print('>>>getCity.py<<<')
     # 沒有做異常
    url = 'https://zip5.5432.tw/cityzip'
    page = get_html_code(url)
    cityList = []
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', id='zip-table')
    for item in table.find_all('a'):
        cityList.append({'city': item.get_text(), 'areas': []})
    # print(cityList)
    get_area(url, cityList)
    
if __name__ == '__main__':
    get_href()
