from parse_functions import *
from get_all_urls_in_txt import get_all_urls_in_txt

def main():
    get_all_urls_in_txt()
    
    with open('urls.txt', 'r') as file:
    	urls = file.readlines()
    
    for counter in range(len(urls)):
    	urls[counter] = urls[counter].replace('\n', '')
    
    products = []
    try:
    	print('Processing...')
    	all_urls = len(urls)
    	current_url = 1
    	for url in urls:
    		products.append(get_product_info(url))
    		print('Finished ', current_url, ' of ', all_urls, ' urls.')
    		current_url += 1
    	write_result(products)
    
    except Exception as e:
    	log_error(str(e)+'\n')

if __name__ == '__main__':
	main()