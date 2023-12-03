# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:09:10 2023

@author: citiz
"""
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import csv
html=requests.get("https://www.mca.gov.cn/mzsj/xzqh/2020/20201201.html")
html.encoding='utf-8'
html_content=html.text
soup=BeautifulSoup(html_content,"html.parser")
tests=soup.find_all("td",{"class":"xl7228320"})
#testa=np.array(tests,dtype=object).reshape(-1,2)
nlist=[]
for test in tests:
	nlist=np.append(nlist,test.get_text())
flist=nlist.reshape(-1,2)
flist[:,1]
flist=pd.DataFrame(flist,columns=['code','city'])
flist=flist.loc[flist['city']!='']
#to get rid of all the spaces in the string
flist['city']=flist['city'].apply(lambda x:x.strip())
flist=flist.loc[[flist['city'].values[i][-1]=='市' for i in range(flist.shape[0])]]
flist=flist[['city','code']]
flist.to_excel(r"C:\Users\citiz\Downloads\citycode1.xlsx")
citylist=dict(flist.values)
for m in ['out', 'in']:
	header=['dest_city']
	with open(r"C:\Users\citiz\Downloads\全国城市级别{}.csv".format(m), "w+", newline="") as csv_file:
		writer=csv.writer(csv_file)
		for k in range(10): #top10
			header.append("in_city{}".format(k))
			header.append("value{}".format(k))
		writer.writerow(header) 
		for index, city_id in enumerate(list(citylist.values())):
			url='https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={}&type=move_{}&date=20231011'.format(city_id,m)
			response=requests.get(url, timeout=10) # #发出请求并json化处理
			time.sleep(1) #挂起一秒
			r=response.text[4:-1]
			data_dict=json.loads(r)
			row=[list(citylist.keys())[index]] ###############
			if data_dict['errmsg']=='SUCCESS':
				data_list=data_dict['data']['list']
				for j in range(10):
					row.append(data_list[j]['city_name'])
					row.append(data_list[j]['value'])
			writer.writerow(row) 








