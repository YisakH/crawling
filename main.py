import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

# MongoDB 연결 설정
client = MongoClient("localhost", 27017)
db = client["crwaling"]
collection = db["ppomppu"]

site_url = 'https://m.ppomppu.co.kr'
keyword = 'qc45'

params = {
    'search_type': 'subject',
    'keyword': keyword
}

def f_get_list():
    new_data_list = []
    
    result_search = requests.get('https://m.ppomppu.co.kr/new/bbs_list.php?id=ppomppu&category=', params=params)
    if result_search.status_code == 200:
        html = result_search.text
        soup = BeautifulSoup(html, 'html.parser')
        times = soup.select('#wrap > div.ct > div.bbs > ul > li > a > div.thmb_N2 > ul > li.exp > time')
        titles = soup.select('#wrap > div.ct > div.bbs > ul > li > a > div.thmb_N2 > ul > li.title > span.cont')
        links = soup.select('a.list_b_01n')

        for i in range(len(titles)):
            board_data = {
                'time': times[i].text,
                'title': titles[i].text.strip(),
                'link': site_url + links[i]['href']
            }
            
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
    time.sleep(10)
