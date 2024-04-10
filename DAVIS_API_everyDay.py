import requests
import json
import pandas as pd
from datetime import datetime
from io import StringIO
import time

def readKeySecret():
    with open('DAVIS_API/API_key.txt','r') as f:
        for line in f:
            key =  line.strip()
    with open('DAVIS_API/API_secret.txt','r') as f:
        for line in f:
            secret =  line.strip()

    return key,secret


#returns measurement data from the last 24h and appends to .csvFile
def getHistoricDataAppend(key,secret,station_id,start,end, end_time, append_time):
    api_url = "https://api.weatherlink.com/v2/historic/"+station_id+"?api-key="+key+"&start-timestamp="+start+"&end-timestamp="+end
    header = {"X-Api-Secret": secret}
    response = requests.get(api_url,headers=header)
    #print(response.json())
    filename= filepath+'Weatherlink_'+station_id+"_"+end_time+"_"
    filename_append= 'Weatherlink_'+station_id+"_"+append_time+"_"

    try:
        i = 0
        df = pd.DataFrame()
        for sensors in response.json()["sensors"]:
            df = pd.DataFrame(sensors['data'])
            df = df.iloc[:, ::-1]
            df.to_csv(filename_append+str(i)+'.csv', encoding='utf-8', sep=';', decimal=",", index=False, mode="a")
            i = i+1
        print(filename_append+" updated")
    except Exception as e:
        print(filename+" not updated")
        print (e)
    return(response)




key,secret = readKeySecret()
station_id = str(170245)

end_timestamp = datetime.now()
end = int(time.mktime(end_timestamp.timetuple()))
start = end - 86400
end_time = end_timestamp.strftime('%Y-%m-%d_%H-%M')
append_time = end_timestamp.strftime('%Y-%m')
data = getHistoricDataAppend(key,secret, station_id,str(start), str(end), end_time, append_time)
print(end_timestamp)

