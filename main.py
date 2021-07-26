import numpy as np
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

class webcrawler():
    def __init__(self,url):
        self.url = url
        self.record_str = []

    def __call__(self):
        # Banned from the website
        header = {"User-Agent":"Chrome/41.0.2227.0"}
        # Get the html architecture
        req_html = requests.get(self.url,headers = header).text
        bs4_html = BeautifulSoup(req_html,"html.parser")
        # find the result box
        result = bs4_html.find(id="results_box")
        tbody = result.find("tbody")
        stock_per_day = tbody.find_all("tr")
        for items in stock_per_day:
            item = items.find_all("td")
            time = datetime.fromtimestamp(float(item[0].get("data-real-value")))
            time_str = datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
            price = float(item[1].get("data-real-value"))
            open = float(item[2].get("data-real-value"))
            high = float(item[3].get("data-real-value"))
            low = float(item[4].get("data-real-value"))
            vol = float(item[5].get("data-real-value"))
            change = item[6].getText("data-real-value")
            #print(time,price,open,high,low,vol,change)
            
            self.record_str.append({'time':time_str,'price':price,'open':open,'high':high,'low':low,'vol':vol,'change':change})
        result = self.list2json(self.record_str)
        return result   

    def time_filter(self,time_start,time_end):
        """
            input: string. the standard is YYYYMMDDHH.
        """
        start = datetime.strptime(time_start,"%Y%m%d%H")
        end = datetime.strptime(time_end,"%Y%m%d%H")
        time_f = []

        for stock in self.record_str:
            if datetime.strptime(stock['time'],'%Y-%m-%d %H:%M:%S') >= start and datetime.strptime(stock['time'],'%Y-%m-%d %H:%M:%S') <= end:
                time_f.append(stock)
    
        return self.list2json(time_f)

    def list2json(self,list):
        json_list = json.dumps(list)
        return json_list
if __name__ == "__main__":
    
    ss= webcrawler(url="https://cn.investing.com/equities/apple-computer-inc-historical-data")
    web = ss()
    #print(web)
    time = ss.time_filter("2021070100","2021072000")
    print(time)
