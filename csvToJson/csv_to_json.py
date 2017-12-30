import csv
import json
import chardet
import urllib.request
import os
import re
from bs4 import BeautifulSoup

# 取得頁面（ex:全國老人福利機構名冊）
def get_html_code(url):
    # 沒有做異常
    url1 = urllib.request.Request(url)
    page = urllib.request.urlopen(url1).read()
    print('Get Page ({0})'.format(url))
    checker = chardet.detect(page)
    page = page.decode(checker['encoding'])
    return page

# 爬頁面（全國老人福利機構名冊），抓取多個csv連結
def get_csv_href(url):
     # 沒有做異常
    page = get_html_code(url)
    hrefList = []
    soup = BeautifulSoup(page, 'html.parser')
    itemAll = soup.find_all('a', string="CSV")
    city = soup.find_all('span', 'ff-desc')
    print('Get download Href')
    # print(itemAll)
    for index, item in enumerate(itemAll):
        hrefList.append({'city': city[index].get_text(), 'href': item.get('href')})
    # print(len(hrefList))
    return hrefList

# 下載後存在本地端
def download_csv(url):
    # 沒有做異常
    csvHrefList = get_csv_href(url)
    print('--Start build csv--')
    path = "./csv"
    if not os.path.isdir(path):
        os.mkdir(path)
    for index, csvHref in enumerate(csvHrefList):
        urllib.request.urlretrieve(csvHref['href'], "./csv/{0}.csv".format(csvHref['city']))
        print('  build {0}.csv'.format(csvHref['city']))

# 讀csv文件
def read_csv(file):
     # 沒有做異常
    csv_rows = []
    encode = detect_encode(file)
    with open(file, 'r', encoding = encode) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
            #csv_row.append({...})
        # print(csv_rows)
        return csv_rows

# 寫json文件
def write_json(data, json_file, jsondir):
    # 沒有做異常
    path = jsondir
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(json_file, "w") as f:
        if(json_file == './json/雲林縣.json'):
            data = change_att(data)
        elif(json_file == './json/高雄市.json'):
            data = change_val(data)
        data = change_word(data)
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))

def change_word(data):
    newData = []
    for item in data:
        if(item['區域別'] == '通宵鎮'):
            item['區域別'] = '通霄鎮'
            print(item['地址'])
        if(item['屬性'] == '財團法人'):
            item['屬性'] = '私立'
        if(item['屬性'] == '公辦民營'):
            item['屬性'] = '公設民營'

        newData.append(item)
    return data

def change_val(data):
    newData = []
    for item in data:
        item['區域別'] = item['區域別'] + '區'
        newData.append(item)
    return newData

def change_att(data):
    newData =[]
    for item in data:
        item['區域別'] = item.pop('鄉鎮別')
        newData.append(item)
    return newData

# 偵測文件 encode
def detect_encode(file):
     # 沒有做異常
    fileread = lambda filename: open(filename, "rb").read()
    fileinfo = chardet.detect(fileread(file))
    return fileinfo['encoding']
    
# csv to json
def csv_to_json(csvdir, jsondir):
    # 沒有做異常
    fileslist = []
    print('--Start transform csv into json--')
    for root, dirs, files in os.walk(csvdir):
        fileslist = files
    # print(fileslist)
    for files in fileslist:
        write_json(read_csv(csvdir + '/{0}.csv'.format(os.path.splitext(files)[0])), jsondir + '/{0}.json'.format(os.path.splitext(files)[0]), jsondir)
        print('  build {0}.json'.format(os.path.splitext(files)[0]))

# 過濾機構名字
def f_ins(name):
    str = name
    m = re.match(r'^\w+(\?)?\w+', str).group().replace('台', '臺')
    return m

# 過濾地址
def f_addr(addr, city, area):
    newaddr = addr.replace('台', '臺')
    if(city == '臺中市'):
        if(newaddr[0:3] != city and newaddr[0:3] != area):
            newaddr = newaddr[3:]
    elif(city == '屏東縣'):
        newaddr = city + area + newaddr
    elif(city == '新北市' or city == '桃園市'):
        newaddr = city + newaddr
    elif(city == '新北市' or city == '苗栗縣'):
        newaddr = city + area + newaddr[3:]
    elif(city == '臺南市'):
         if(area == newaddr[0:2]):
            newaddr = city + newaddr
    elif(city == '宜蘭縣'):
        if(newaddr[0:3] != city and newaddr[0:2] != area):
            newaddr = city + area + newaddr
    else:
        if(newaddr[0:3] != city and newaddr[0:2] != area):
            if(newaddr[0:3] == '307新'):
                newaddr = newaddr[3:]
            newaddr = newaddr[5:]
    return newaddr

# 過濾經緯度
def checkll(l_value,l):
    if('latitude' == l and l_value == '' or l_value == '查無經緯度'):
        return '25.006743'
    elif('longitude' == l and l_value == '' or l_value == '查無經緯度'):
        return '121.512882'
    else:
        return l_value

def fill_num(ins):
    newInsID = "{0:0>4}".format(int(ins)) + '0'
    return str(newInsID)

def get_newInsID(city, area, ins):
    ps = get_postalCode(city ,area)
    newCode = ps + fill_num(ins)
    return newCode

def get_postalCode(city, area):
    cityJson = json.loads(open('city.json').read())

    for c in cityJson:
        if(city == c['city']):
            for a in c['areas']:
                if(area[0:2] == a['area_name'][0:2]):
                    return a['postal_code']

# 過濾每一屬性資料
def read_json(file):
    institutions = json.loads(open(file).read())
    newIns = []
    city = os.path.splitext(os.path.basename(file))[0].strip()
    for institution in institutions:
        ins = {}
        ins['ins_id'] = get_newInsID(city, institution['區域別'].strip(), institution['編號'].strip())
        ins['ins_type'] = institution['屬性'].strip()
        ins['ins_name'] = f_ins(institution['機構名稱'].strip())
        ins['agent'] = institution['負責人'].strip()
        ins['phone'] = institution['電話'].strip()
        ins['capacity'] = institution['收容對象'].strip()
        ins['num_bed'] = institution['核定收容人數'].strip()
        ins['city'] = city
        ins['area'] = institution['區域別'].strip()
        ins['address'] = f_addr(institution['地址'].strip(), city, institution['區域別'].strip())
        ins['latitude'] = float(checkll(institution['Latitude'], 'latitude'))
        ins['longitude'] = float(checkll(institution['Longitude'], 'longitude'))
        
        newIns.append(ins)
    return [dict(t) for t in set([tuple(d.items()) for d in newIns])]

# 重寫成新的json
def rewrite_json(data, json_file, fjsondir):
    path = fjsondir
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(json_file, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))

# 過濾成所需要的資料
def filter_json(jsondir, fjsondir):
    # 沒有做異常
    fileslist = []
    print('--Start filter the data--')
    for root, dirs, files in os.walk(jsondir):
        fileslist = files
    for files in fileslist:
        rewrite_json(read_json(jsondir + '/{0}'.format(files)), fjsondir + '/{0}'.format(files), fjsondir)
        print('  build new {0}.json'.format(os.path.splitext(files)[0]))

def main():
    print('>>>csv_to_json.py<<<')
    try:
        download_csv('https://data.gov.tw/dataset/8572')
        csv_to_json('./csv', './json')
        filter_json('./json', './filterJson')
    except KeyboardInterrupt as e:
        print('KeyboardInterrupt: 幹嘛中斷我?')
    finally:
        print('END')

if __name__ == '__main__':
    main()

