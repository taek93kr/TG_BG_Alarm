# 6049342646:AAEyzOnP-DsB4hMKFFr4j-EfgjiEYNIGdug

# -*- coding utf-8 -*-
from bs4 import BeautifulSoup
import requests

url = "https://boardlife.co.kr/bbs_list.php?tb=board_used"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

beforePosts = []

for i in range(3,13):
    beforePost = soup.select_one('#container > main > div > div.area-common > article:nth-child('+str(i)+') > div > a > strong').text
    # print(beforePost)
    beforePosts.append(beforePost)

# print(set(beforePosts))
beforeSet = set(beforePosts)
print(beforeSet)