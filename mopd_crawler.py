import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

if not os.path.isdir('./mops'):
    os.mkdir('./mops')
headers = {'Referer': 'https://mops.twse.com.tw/mops/web/t163sb04','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
payload = {
    'encodeURIComponent': 1,
    'step': 1,
    'firstin': 1,
    'off': 1,
    'isQuery': 'Y',
    'TYPEK': 'sii', # sii 上市 / otc 上櫃
    'year': 107,
    'season': '02',}
resp = requests.post('https://mops.twse.com.tw/mops/web/ajax_t163sb04', data=payload, headers=headers, timeout=2)
soup = BeautifulSoup(resp.text, 'html.parser')
tables = soup.find_all('table')
for k in range(1,len(tables)):
    data=[]
    rows = tables[k].find_all('tr')
    columns = rows[0].find_all('th')
    columns_list = [columns[i].text for i in range(len(columns))]
    print(len(rows)-1)
    for j in range(1,len(rows)):
        data_row = [rows[j].find_all('td')[i].text for i in range(len(columns))]
        data.append(data_row)
        #print(data_row)
        df = pd.DataFrame(data=data, columns=columns_list)
        df.to_csv('./mops/{}.csv'.format(str(payload['year'])+payload['season']+'_'+str(k)), index=0, encoding='utf-8-sig')
