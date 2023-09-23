#

# -*- coding utf-8 -*-
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import datetime
from datetime import datetime
import telegram
import asyncio
import time


tg_token = '6049342646:AAEyzOnP-DsB4hMKFFr4j-EfgjiEYNIGdug'
chat_id = 1092021314
async def send_msg(msg):
    bot = telegram.Bot(tg_token)
    await bot.send_message(chat_id=chat_id, text=msg)

URLs = defaultdict(bool)
key_words = ['아컴', '아딱', '마블']

with open('URL.txt', 'r') as file:
    for line in file:
        line = line.strip()  # 줄바꿈 제거
        URLs[line] = True

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
asyncio.run(send_msg(formatted_datetime))
while True:
    url = "https://boardlife.co.kr/bbs_list.php?tb=board_used"
    html = requests.get(url)
    soup = BeautifulSoup(html.content.decode('euc-kr', 'replace'), "html.parser")

    for i in range(33):
        item = '#main-community-div > a:nth-child(%d)' % i

        post_title = soup.select_one(item)
        if post_title is not None:
            # print(i, post_title, "-----------\n\n")
            post_url = 'https://boardlife.co.kr/' + post_title.get('href')

            category_element = post_title.find(class_='category_icon')
            if category_element:
                category_value = category_element.text.strip()
                # print(category_value, post_url)
                if "판매" in category_value or "나눔" in category_value:
                    post = requests.get(post_url)
                    post_soup = BeautifulSoup(post.content.decode('euc-kr', 'replace'), "html.parser")
                    contents = post_soup.select_one('#bbs-review-wrapper')
                    # print(category_value, contents)
                    # print("-------------------------\n\n\n")

                    # if '아컴' in contents.text or '아딱' in contents.text:
                    # if any(keyword in contents.text for keyword in key_words):
                    included_keywords = [keyword for keyword in key_words if keyword in contents.text]
                    if included_keywords:
                        if not URLs[post_url]:
                            URLs[post_url] = True
                            asyncio.run(send_msg("[%s] %s %s" % (category_value, str(included_keywords), post_url)))
                            with open('URL.txt', 'a') as file:  # 파일에 URL 추가
                                file.write(post_url + "\n")
                        else:
                            pass
            else:
                # print("category_icon class not found.")
                pass

    # 현재 날짜와 시간을 가져옵니다.
    current_datetime = datetime.now()
    # 원하는 형식으로 출력
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    print(formatted_datetime)
    time.sleep(60)