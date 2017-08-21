import requests, json, codecs
from urllib.parse import urlencode

url = 'http://apis.baidu.com/heweather/pro/weather?'

data = {
    "city":"dongsheng"
}
param = urlencode(data)
url = url + param

headers = {
    "apikey" : "f244927c0c502d71cd5c86d15b678d95"
}

res = requests.get(url,headers=headers).json()
result = res['HeWeather data service 3.0']

alarmInfo = {}

with codecs.open("alarmInfo.json",'r') as f:
    alarm_pic = json.load(f)

if 'alarms' in result[0].keys():
    alarmInfo['status'] = 1
    alarmInfo['data'] = alarm_pic[result[0]['alarms'][0]['type']][result[0]['alarms'][0]['level']]
else:
    alarmInfo['status'] = 0
    alarmInfo['data'] = ''

file_path = "F:\\nginx\html\\weatherStation\\alarmInfo.json"
with codecs.open(file_path,'w','utf-8') as f:
	f.write(json.dumps(alarmInfo))
	f.close()