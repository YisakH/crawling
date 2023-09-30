import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import sys
import os


category = sys.argv[1]
#category = '5'

"""
if len(sys.argv) != 2:
    print("Insufficient arguments")
    sys.exit()
"""

mongoUrl = os.environ['MONGO_URL']
mongoPort = os.environ['MONGO_PORT']
mongoDb = os.environ['MONGO_DB']
mongoCol = os.environ['MONGO_COL']

# MongoDB 연결 설정
client = MongoClient(mongoUrl, int(mongoPort))
db = client[mongoDb]
collection = db[mongoCol]

site_url = 'https://www.ppomppu.co.kr/zboard/zboard.php/'
keyword = ''

params = {
    #'search_type': 'subject',
    'keyword': keyword,
    'category': category
}

def f_get_list():
    new_data_list = []
    
    result_search = requests.get('https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu', params=params)
    if result_search.status_code == 200:
        html = result_search.text
        soup = BeautifulSoup(html, 'html.parser')
        
        title_elems = soup.select('tr > td > div > a > font')
        titles = [elem.get_text(strip=True) for elem in title_elems][:20]
            
        date_elems = soup.select('td.eng.list_vspace[title]')
        dates = [elem['title'] for elem in date_elems]
        #dates = [elem['title'] for elem in date_elems][1:]
        
        # a 태그를 선택합니다.
        a_elems = soup.select('tr > td > div > a')

        # 각 a 태그에서 href 속성을 추출합니다.
        links = [a['href'] for a in a_elems if 'href' in a.attrs][:20]




        for i in range(len(titles)):
            board_data = {
                'time': dates[i],
                'title': titles[i],
                'link': site_url + links[i],
                'category': int(category)
            }
            
            if(board_data['title'].find('[키워드 알림]') >= 0):
                continue
                
            
            # Check if data exists in the database
            if not collection.find_one(board_data):
                new_data_list.append(board_data)
                print(f"New Data Found!\n작성시간: {board_data['time']}\n제목: {board_data['title']}\n링크: {board_data['link']}")

    else:
        print(result_search.status_code)
    
    # If new data exists, insert into the database
    if new_data_list:
        collection.insert_many(new_data_list)

while True:
    f_get_list()
    time.sleep(180)
