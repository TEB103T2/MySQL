import pymongo 
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import csv

cluster = MongoClient('mongodb+srv://crawler:!QAZ2wsx@cluster0.k1oua.mongodb.net/wear?retryWrites=true&w=majority')
db = cluster['wear']
collection = db['Mondel_W']
results = collection.find({'Mondel_Rank': '62'}) #62,88
feature = []

for result in results: 
    for sets in result['SET']:
        feature.append(sets["Set_Url"])




headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
'Referer': 'https://wear.tw/ranking/user/'
}

likeList = []
for url in feature:
    tempList = []
    tempList2 = []
    for page in range(1,500):
        urlL = url + 'like/?pageno=' + f'{page}'
        resL = requests.get(urlL, headers=headers)
        soupL = BeautifulSoup(resL.text, 'lxml')
        userList = soupL.find_all('li', class_='list')
        for u in userList:
            userId = u.find('a').get('href').split('/')[1]
            if userId not in tempList:
                tempList.append(userId)
                tempList2.append([url.split('/')[-3] + "_" + url.split('/')[-2],userId])
            else:
                break
        else:
            continue
        break
    likeList.append(tempList2)
# print(likeList)
with open('likeuser.csv', 'w', newline='',  encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    for like in likeList:
        for i in like:
            writer.writerow([i[0],i[1]])


