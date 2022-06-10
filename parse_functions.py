import requests
from bs4 import BeautifulSoup

def log_error(error):
	with open('logs.txt', 'a', encoding='utf-8') as file:
		file.write(error+'\n')

def safe_tag_text_parse(tag):
	if tag:
		return tag.text
	else:
		return None

def get_base_url(url):
	position = 0
	slash_count = 0
	while (slash_count<3) and (position<len(url)):
		if url[position]=='/':
			slash_count+=1
		position+=1
	base_url = url[:position-1:]
	return base_url

def replace_duplicates(list_with_duplicates):
	list_temp = []
	for element in list_with_duplicates:
		if not element in list_temp:
			list_temp.append(element)
	return list_temp

def get_category_list(url):
	try:
		print('Collecting category list...')
		base_url = get_base_url(url)
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
		log_error(str(e)+'\n'+url+'\n')
		return None

def get_category_urls(url):
	try:
		base_url = get_base_url(url)
		urls = []
		next_page = url
		while next_page:
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
		log_error(str(e)+'\n'+url+'\n')
		return None

def get_product_info(url):
	try:
		base_url = get_base_url(url)
		raw_data = requests.get(url)
		soup = BeautifulSoup(raw_data.text, 'html.parser')
		title = soup.find('h1', id ='pagetitle')
		title = safe_tag_text_parse(title)
		article = soup.find('div', class_="article iblock").find('span', class_="value")
		article = safe_tag_text_parse(article)
		description = soup.find('div', class_="detail_text")
		description = safe_tag_text_parse(description)
		properties = soup.find('table', class_="props_list")
		if properties:
			properties_names = soup.find('table', class_="props_list").find_all('span', itemprop="name")
			properties_values = soup.find('table', class_="props_list").find_all('span', itemprop="value")
			properties = [['']*len(properties_names), ['']*len(properties_values)];
			position = 0
			for line in properties_names:
				properties[0][position] = line.text.replace('\n', '').replace('\t', '')
				position += 1
			position = 0
			for line in properties_values:
				properties[1][position] = line.text.replace('\n', '').replace('\t', '')
				position += 1
			properties_temp = ''
			for index in range(len(properties[0])):
				properties_temp+=str(properties[0][index])+': '+str(properties[1][index])+'\n'
			properties = properties_temp
		img_temp = soup.find('li', id="photo-0", class_="current").find('img').get('data-src')
		img_url = base_url+str(img_temp	)
		price_temp = soup.find('div', class_="price")
		price = price_temp.get('data-value')
		currency = price_temp.get('data-currency')
		categories_temp = soup.find('div', class_="breadcrumbs", id="navigation")
		categories_temp = categories_temp.find_all('div', class_="bx-breadcrumb-item")
		categories = [None]*(len(categories_temp[2::]))
		for index in range(len(categories_temp[2::])):
			categories[index] = safe_tag_text_parse(categories_temp[index+2].find('span', itemprop="name"))
		expandables_temp = soup.find('li', class_="tab EXPANDABLES_wrapp")
		expandables = ''
		if expandables_temp:
			expandables_temp = expandables_temp.find_all('li', class_="catalog_item")
			if expandables_temp:
				for product in expandables_temp:
					exp_product = product.find('div', class_="item-title").find('span')
					expandables+=safe_tag_text_parse(exp_product)+'\n'
		if not expandables:
			expandables = None

		product = {'title':title, 'article':article, 'description':description,
		'properties':properties, 'img_url':img_url, 'price':price, 'currency':currency,
		'number_of_categories':len(categories), 'expandables':expandables}
		for index in range(len(categories)):
			product.update({'category{}'.format(index+1):categories[index]})
		return product
	except Exception as e:
		log_error(str(e)+'\n'+url+'\n')
		return None

def write_result(products):
	with open('out.csv', 'w', encoding='utf-8') as file:
		max_number_of_categories = 0
		for product in products:
			if product and product['number_of_categories'] and product['number_of_categories']>max_number_of_categories:
				max_number_of_categories = product['number_of_categories']
		category_column_headers = ''
		for index in range(max_number_of_categories):
			category_column_headers+='category{}`'.format(index+1)
		category_column_headers = category_column_headers[:len(category_column_headers)-1]+'\n'
		file.write('title`article`description`properties`img_url`price`currency`expandables`'+category_column_headers)
		for product in products:
			if product:
				file.write('"'+str(product['title']).replace('"', '""')+'"`"'+str(product['article'])+
					'"`"'+str(product['description']).replace('"', '""')+'"`"'+
					str(product['properties']).replace('"', '""')+'"`'+str(product['img_url'])+'`"'+
					str(product['price'])+'"`'+str(product['currency'])+'`"'+str(product['expandables']).replace('"', '""')+'"`')
				product_categories = ''
				for index in range(max_number_of_categories):
					product_categories+='"'+str(product.get('category{}'.format(index+1))).replace('"', '""')+'"`'
				product_categories+='\n'
				file.write(product_categories)