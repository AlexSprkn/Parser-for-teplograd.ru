import requests
from bs4 import BeautifulSoup

def get_category_list(url):
	try:
		print('Collecting category list...')
		position = 0
		slash_count = 0
		while (slash_count<3) and (position<len(url)):
			if url[position]=='/':
				slash_count+=1
			position+=1
		base_url = url[:position-1:]
		raw_data = requests.get(url)
		soup = BeautifulSoup(raw_data.text, 'html.parser')
		data_block = soup.find('div', class_="menu_top_block catalog_block")
		if data_block:
			data_block1=data_block.find_all('a', class_="icons_fa parent")
			urls = []
			for category_url in data_block1:
				category_url1 = base_url+category_url.get('href')
				category_name = category_url.text
				urls.append({'category_url':category_url1, 'category_name':category_name})
			return urls
		else:
			return None
	except Exception as e:
		print(str(e))
		return None
