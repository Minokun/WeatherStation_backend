import requests, json, codecs
from urllib.parse import urlencode

url = 'http://apis.baidu.com/netpopo/weather/query?'

data = {
    "city":"东胜区",
    "cityid":2201,
    "citycode":101080713
}
param = urlencode(data)
url = url + param

headers = {
    "apikey" : "f244927c0c502d71cd5c86d15b678d95"
}

res = requests.get(url,headers=headers).json()
result = res['result']

key = ['weather_s','weather_e','temphigh','templow','winddirect','windpow','quality','detail']
value = [result['daily'][0]['night']['weather'],result['daily'][0]['day']['weather'],result['temphigh'],result['templow'],result['winddirect'],result['daily'][0]['day']['windpower'],result['aqi']['quality'],result['index'][1]['detail']]

file_path = "F:\\nginx\html\\weatherStation\\weatherData.json"
with codecs.open(file_path,'w','utf-8') as f:
	f.write(json.dumps(dict(zip(key,value))))
	f.close()