from parse_functions import *

def get_all_urls_in_txt():
	start_url = 'https://www.teplograd.ru/'
	urls = []
	categories = get_category_list(start_url)
	for iii in range(len(categories)):
		print(categories[iii]['category_name'], f', category No {iii+1} of {len(categories)}:', sep='')
		category_urls = get_category_urls(categories[iii]['category_url'])
		for jjj in category_urls:
			urls.append(jjj)
	with open('urls.txt', 'w') as file:
		for url in urls:
			file.write(url+'\n')
		print("Urls quantity: ", len(urls))