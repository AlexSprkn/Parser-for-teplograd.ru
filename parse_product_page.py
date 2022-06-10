import requests
from bs4 import BeautifulSoup

def safe_tag_text_parse(tag):
	if tag:
		return tag.text
	else:
		return None

def get_product_info(url):
	try:
		position = 0
		slash_count = 0
		while (slash_count<3) and (position<len(url)):
			if url[position]=='/':
				slash_count+=1
			position+=1
		base_url = url[:position-1:]
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
		img_url = base_url+soup.find('li', id="photo-0", class_="current").find('a').get('href')
		price_temp = soup.find('div', class_="price")
		print(bool(price_temp))
		price = price_temp.get('data-value')
		currency = price_temp.get('data-currency')
		#return ProductInfo(title, article, description, properties, img_url, price, currency)
		return {'title':title, 'article':article, 'description':description, 'properties':properties, 'img_url':img_url, 'price':price, 'currency':currency}
	except Exception as e:
		print(str(e))
		return None
