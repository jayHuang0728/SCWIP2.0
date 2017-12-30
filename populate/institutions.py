#from populate import base
import json
from os import walk, path
from backend.models import Institution, City, Capacity, Institutions_Unit, Aqi

def allInit():
    Institution.objects.all().delete()
    Aqi.objects.all().delete()
    City.objects.all().delete()
    Capacity.objects.all().delete()
    Institutions_Unit.objects.all().delete()

def read_json(dirname, file):
    return json.loads(open(dirname + '/' + file).read())

def fillCity(dirname, cityJson ):
    cityJsonContent = read_json(dirname, cityJson)
    for items in cityJsonContent:
        cityName = items['city']
        for item in items['areas']:
            city = City()
            city.city_id = item['postal_code']
            city.city_name = cityName
            city.area_name = item['area_name']
            city.save()
    print('City table done!')

def clasify(Area):
    if(Area == '北部'):
        return ['臺北市', '基隆市', '新北市', '桃園市']
    if(Area == '花東'):
        return ['花蓮縣', '臺東縣']
    if(Area == '高屏'):
        return ['高雄市', '屏東縣']
    if(Area == '雲嘉南'):
        return ['雲林縣', '嘉義縣', '臺南市']
    if(Area == '中部'):
        return ['臺中市', '彰化縣', '南投縣']
    if(Area == '竹苗'):
        return ['新竹縣', '苗栗縣']
    if(Area == '澎湖'):
        return ['澎湖縣']
    if(Area == '金門'):
        return ['金門縣']
    if(Area == '宜蘭'):
        return ['宜蘭縣']
    else:
        pass

def fillAqi(dirname, aqiJson, cityJson):
    a = 0 
    print('AQI populate')
    aqiContent = read_json(dirname, aqiJson)
    cityJsonContent = read_json(dirname, cityJson)
    
    for aqiList in  aqiContent:
        Area = clasify(aqiList['Area'])
        if Area != None:
            for items in Area:
                for city in cityJsonContent:
                    cityName = city['city']    
                    if items == cityName:
                        for area in city['areas']:
                            # print(area['postal_code'])       
                            aqi = Aqi()
                            aqi.aqi_area = cityName
                            aqi.aqi_index = aqiList['AQI']
                            aqi.city_id = City.objects.get(city_id = area['postal_code'])
                            aqi.save()
                    else:
                       pass
        else:
            pass
    print('AQI table done!')

        
    #         for item in Area:
    #             a = a + 1
    #             aqi = Aqi()
    #             aqi.aqi_id = str(a) 
    #             aqi.aqi_area = item
    #             aqi.aqi_index = items['AQI']
    #             q = City.objects.filter(city_name='Area')
    #             aqi.city_id = q.city_id
    #             aqi.save()
    #     else:
    #         pass
    # print('AQI table done!')

def fillInstitution(dirname):
    for root, dirs, files in walk(dirname):
        fileslist = files
    CapItems = set()
    cap = Capacity()
    c = 0

    for file in fileslist:
        jsonContent = read_json(dirname, file)
        for insContent in jsonContent:
            # print(insContent)
            ins = Institution()
            ins.ins_id = insContent['ins_id']
            ins.ins_type = insContent['ins_type']
            ins.ins_name = insContent['ins_name']
            ins.agent = insContent['agent']
            ins.phone = insContent['phone']
            ins.city = City.objects.get(city_id=insContent['ins_id'][:3])
            ins.address = insContent['address']
            ins.latitude = insContent['latitude']
            ins.longitude = insContent['longitude']
            CapItems.add(insContent['capacity'])
            ins.save()
    print('Institution table done!')

    for CapItem in CapItems:
        c = c + 1
        cap.cap_id = str(c) + '0'
        cap.cap_name = CapItem
        cap.save()
    print('Capacity table done!')

    for file in fileslist:
        jsonContent = read_json(dirname, file)
        for insContent in jsonContent:
            ins_unit = Institutions_Unit()
            ins_unit.Ins_id = Institution.objects.get(ins_id=insContent['ins_id'])
            ins_unit.Cap_id = Capacity.objects.get(cap_name=insContent['capacity'])
            ins_unit.num_bed = insContent['num_bed']
            ins_unit.save()
    print('Institutions_Unit table done!')


def populate():
    print('Populating..')
    allInit()
    fileslist = []
    dirname = '/Users/open159259/SCWIP_Ver1.0/csvToJson'
    filterJsonDir = 'filterJson'
    cityJson = 'city.json'
    aqiJson = 'AQI.json'
    fillCity(dirname, cityJson)
    fillInstitution(dirname + filterJsonDir)
    fillAqi(dirname, aqiJson, cityJson)

if __name__ == '__main__':
    populate()
