from parse_product_page import *
from get_category_urls import *
from get_category_list import *

def get_all_urls_in_txt():
	start_url = 'https://www.teplograd.ru/'
	categories = get_category_list(start_url)
	for iii in range(len(categories)):
		print(categories[iii]['category_name'], ':')
		category_urls = get_category_urls(categories[iii]['category_url'])
		for jjj in category_urls:
			urls.append(jjj)
	with open('urls.txt', 'w') as file:
		for url in urls:
			file.write(url+'\n')
		print("Urls quantity: ", len(urls))