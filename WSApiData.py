
# coding: utf-8

# In[2]:


def apiData():

    import requests
    import json
    import time
    import codecs

    current_time_unix = int(time.time()) - 8 * 3600 - 5 * 60
    current_time = time.strftime("%Y%m%d%H",time.localtime(current_time_unix))
    current_minutes = time.strftime("%M",time.localtime(current_time_unix)) 
    minutes = int(int(current_minutes)/5) * 5
    minutes = str(minutes) if minutes >= 10 else "0" + str(minutes)
    time_data = current_time + minutes + "00"

    url_temp = "http://10.62.89.55/cimiss-web/api?userId=BEHT_BFDS_dsqqxj&pwd=ds53543&interfaceId=getSurfEleByTimeAndStaID&dataCode=SURF_CHN_MAIN_MIN&elements=TEM&times=" + time_data + "&staIds=53543,C3024,C3023&limitCnt=30&dataFormat=json"
    url_other = "http://10.62.89.55/cimiss-web/api?userId=BEHT_BFDS_dsqqxj&pwd=ds53543&interfaceId=getSurfEleByTimeAndStaID&dataCode=SURF_CHN_OTHER_MIN&elements=TEM_Max,TEM_Min,PRE_1h,WIN_D_Avg_10mi,WIN_S_Avg_10mi&times=" + time_data + "&staIds=53543,C3024,C3023&limitCnt=30&dataFormat=json"
    res_temp = requests.get(url_temp).json()  
    res_other = requests.get(url_other).json()  
    for key,item in enumerate(res_temp['DS']):
        res_other['DS'][key]['TEM'] = item['TEM']

    res_deal = []
    for item in res_other['DS']:
        item['direction'] = directionJudge(int(item['WIN_D_Avg_10mi']))
        res_deal.append(item)

    result = res_deal + sqlServer()

    file_path = "F:\\nginx\html\\weatherStation\\apiData.json"
    with codecs.open(file_path,'w','utf-8') as f:
        f.write(json.dumps(result))
        f.close()

def sqlServer():
    import pymssql

    conn=pymssql.connect(host='DSQXJ-E3FDAFDAF',user='sa',password='123',database='CAWSAnyWhereServer')

    cursor = conn.cursor()

    list_header = ['WIN_D_Avg_10mi','WIN_S_Avg_10mi','TEM','TEM_Max','TEM_Min']

    cursor.execute("select top 1 AE,AF,BC,BCMX,BCMN from MD1001 ORDER BY TT DESC")
    row = cursor.fetchone()
    data_1 = dict(zip(list_header,map(validate,list(row))))
    data_1['PRE_1h'] = 0
    data_1['direction'] = directionJudge(data_1['WIN_D_Avg_10mi'])
    data_1['WIN_S_Avg_10mi'] = data_1['WIN_S_Avg_10mi'] / 10

    cursor.execute("select top 1 AE,AF,BC,BCMX,BCMN from MD1002 ORDER BY TT DESC")
    row = cursor.fetchone()
    data_2 = dict(zip(list_header,map(validate,list(row))))
    data_2['PRE_1h'] = 0
    data_2['direction'] = directionJudge(data_2['WIN_D_Avg_10mi'])
    data_2['WIN_S_Avg_10mi'] = data_2['WIN_S_Avg_10mi'] / 10

    cursor.execute("select top 1 AE,AF,BC,BCMX,BCMN from MD1003 ORDER BY TT DESC")
    row = cursor.fetchone()
    data_3 = dict(zip(list_header,map(validate,list(row))))
    data_3['PRE_1h'] = 0
    data_3['direction'] = directionJudge(data_3['WIN_D_Avg_10mi'])
    data_3['WIN_S_Avg_10mi'] = data_3['WIN_S_Avg_10mi'] / 10

    data_sqlserver = []
    data_sqlserver.append(data_1)
    data_sqlserver.append(data_2)
    data_sqlserver.append(data_3)

    cursor.close()
    conn.close()

    return data_sqlserver

def validate(num):
        if abs(int(num)) > 600:
            res = ''
        elif abs(int(num)) > 60 and abs(int(num)) < 600:
            res = int(num) / 10
        else:
            res = num
        return res

def directionJudge(num):
    if num >= 337.5 or num <= 22.5:
        direction = "北风"
    elif num > 22.5 and num <= 67.5:
        direction = '东北风'
    elif num > 67.5 and num <= 112.5:
        direction = '东风'
    elif num > 112.5 and num <= 157.5:
        direction = '东南风'
    elif num > 157.5 and num <= 202.5:
        direction = '南风'
    elif num > 202.5 and num <= 247.5:
        direction = '西南风'
    elif num > 247.5 and num <= 295.5:
        direction = '西风'
    elif num > 295.5 and num <= 337.5:
        direction = '西北风'
    return direction

if __name__ == "__main__":
    apiData()