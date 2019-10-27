import requests
from bs4 import BeautifulSoup
import pymongo as mongo

html = requests.get('https://www.naver.com/').text
soup = BeautifulSoup(html,'html.parser')

title_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')

client = mongo.MongoClient("mongodb://localhost:27017/")
db = client["db"]
keyword = db["naverKeyword"]


for idx, title in enumerate(title_list , 1):
    str_menu = {"no":idx, "keyword":title.text}
    person_id = keyword.insert_one(str_menu).inserted_id
    print(idx, title.text)
