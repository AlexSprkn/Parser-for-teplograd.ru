import requests
from bs4 import BeautifulSoup

def get_category_urls(url):
	try:
		position = 0
		slash_count = 0
		print('Collecting urls...')
		while (slash_count<3) and (position<len(url)):
			if url[position]=='/':
				slash_count+=1
			position+=1
		base_url = url[:position-1:]
		urls = []
		next_page = url
		while next_page:
			print("Page: ", slash_count-2)
			slash_count+=1
			raw_data = requests.get(next_page)
			soup = BeautifulSoup(raw_data.text, 'html.parser')
			next_page = soup.find('a', class_="flex-next")
			block = soup.find('div', class_="catalog_block items block_list")
			current_page_products_list = block.find_all('div', class_="item-title")
			for product in current_page_products_list:
				urls.append(base_url+product.find('a').get('href'))
			if next_page:
				next_page = base_url+next_page.get('href')
		return urls
	except Exception as e:
		print(str(e))
		return None

url = 'https://www.teplograd.ru/catalog/kotly'

urls = get_category_urls(url)
print(len(urls))
