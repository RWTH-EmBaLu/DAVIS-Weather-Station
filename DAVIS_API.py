import requests
import json
import pandas as pd
from datetime import datetime
from io import StringIO
import time


#read key and secret stored in API_key.txt and API_secret.txt for authentification
def readKeySecret():
    with open('DAVIS_API\API_key.txt','r') as f:
        for line in f:
            key =  line.strip()
    with open('DAVIS_API\API_secret.txt','r') as f:
        for line in f:
            secret =  line.strip()

    return key,secret


#returns all the wheaterlink stations, save as .csv
def getStations(key,secret):
    api_url = "https://api.weatherlink.com/v2/stations?api-key="+key
    header = {"X-Api-Secret": secret}
    response = requests.get(api_url,headers=header)
    print(response.json())
    try:
        df = pd.DataFrame(response.json())
        date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        df.to_csv('DAVIS_API\Weatherlink_pods_'+date+'.csv', encoding='utf-8', sep=';', decimal=",", index=False)
        print("Weatherlink_pods_.csv updated")
    except Exception as e:
        print("Weatherlink_pods_.csv not updated")
        print(e)
    return(response.json())

#returns sensor data from one station 
def getSensors(key,secret,station_id):
    api_url = "https://api.weatherlink.com/v2/current/"+station_id+"?api-key="+key
    header = {"X-Api-Secret": secret}
    response = requests.get(api_url,headers=header)
    print(response.json())
    date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename= 'DAVIS_API\Weatherlink_'+station_id+"_"+date+'.csv'
    try:
        i = 0
        df = pd.DataFrame()
        for sensors in response.json()["sensors"]:
            df = pd.DataFrame(sensors['data'])
            df = df.iloc[:, ::-1]
            filename= 'DAVIS_API\Weatherlink_'+station_id+"_"+date+"_"+str(i)+'.csv'
            df.to_csv(filename, encoding='utf-8', sep=';', decimal=",", index=False)
            i = i+1
        print(filename+" updated")
    except Exception as e:
        print(filename+" not updated")
        print (e)
    return(response)


#return historic measurement date between start and end time , appends at the end of the .csv
def getHistoricData(key,secret,station_id,start,end,start_time, end_time):
    api_url = "https://api.weatherlink.com/v2/historic/"+station_id+"?api-key="+key+"&start-timestamp="+start+"&end-timestamp="+end
    header = {"X-Api-Secret": secret}
    response = requests.get(api_url,headers=header)
    #print(response.json())
    #filename= 'DAVIS_API\Weatherlink_'+station_id+"_"+start_time+'_-_'+end_time+'_'
    filename= 'DAVIS_API\Weatherlink_'+station_id+"_"+start_time+"_"

    try:
        i = 0
        df = pd.DataFrame()
        for sensors in response.json()["sensors"]:
            df = pd.DataFrame(sensors['data'])
            df = df.iloc[:, ::-1]
            df.to_csv(filename+str(i)+'.csv', encoding='utf-8', sep=';', decimal=",", index=False, mode = 'a')
            i = i+1
        print(filename+" updated")
    except Exception as e:
        print(filename+" not updated")
        print (e)
    return(response)



key,secret = readKeySecret()
station_id = str(170245)  #ID of the weatherlink station

getStations(key,secret)
data = getSensors(key,secret, station_id)


for i in range(30): # get historic data for every day of January 2024
    start_timestamp = datetime(2024, 1, i+1, 0, 0) 
    start = int(time.mktime(start_timestamp.timetuple()))
    start_time = start_timestamp.strftime('%Y-%m')
    end_timestamp = datetime(2024, 1, i+2, 0, 0) 
    end = int(time.mktime(end_timestamp.timetuple()))
    end_time = end_timestamp.strftime('%Y-%m')
  #  data = getHistoricData(key,secret, station_id,str(start), str(end), start_time, end_time)
    print(start_timestamp)
#data = getHistoricDataTXT(key,secret, station_id,str(start), str(end) )  #timestamps max 24h