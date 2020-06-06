import requests
from bs4 import BeautifulSoup
import csv
import string

URL = 'https://vk.com/club188839994'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
FILE = 'cars.csv'
HOST ='vk.com'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='_post post page_block all own post--with-likes closed_comments deep_active')

	cars = []

	for item in items:
		link = item.find('a', class_='page_post_thumb_wrap')
		if link:
			link = str(link)
			nach = link.find('background-image: url')
			konec = link.find(');')
			link = link[nach+22:konec]
		video = item.find('div',class_='page_post_sized_thumbs')
		if video:
			video = str(video)
			nach = video.find('href=')
			konec = video.find('onclick')
			video = video[nach+6:konec-2]
			video = HOST + video
		if len(str(video)) > 100:
			video = None	
		cars.append({
			'author' : item.find('a', class_='author').get_text(strip=True),
			'date' : item.find('div', class_='post_date').get_text(strip=True),
			'text' : item.find('div', class_='wall_post_text').get_text(strip=True),
			'image': link,
			'video': video,
			})

	return(cars)



def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for item in items:
            writer.writerow([item['author'], item['date'], item['text'],item['image'], item['video']])

def parse():
	html = get_html(URL)
	cars = []
	if html.status_code == 200:	
		cars.extend(get_content(html.text))
		save_file(cars,FILE)		
	else:
		print('Error')


parse()
