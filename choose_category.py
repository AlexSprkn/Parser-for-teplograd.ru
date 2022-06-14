from parse_functions import *
import datetime

def main():
    start_url = 'https://www.teplograd.ru/'
    categories = get_category_list(start_url)
    urls = []
    user_choice = -1

    while user_choice not in range(1, len(categories)+1):
        user_choice = input('Enter the number of category you want to save in csv: ')
        for char in user_choice:
            if not char.isdigit():
                break
        else:
            user_choice = int(user_choice)

    print(f'Collecting urls of category \"{categories[user_choice-1]["category_name"]}\"')
    category_urls = get_category_urls(categories[user_choice-1]['category_url'])
    urls = category_urls
    
    products = []
    try:
        print('Processing...')
        all_urls = len(urls)
        current_url = 1
        for url in urls:
            products.append(get_product_info(url))
            print('Finished ', current_url, ' of ', all_urls, ' urls.')
            current_url += 1
        print('Writing results...')
        now = str(datetime.datetime.today())[:19].replace(':', '.')
        write_result(products, filename=categories[user_choice-1]["category_name"] + 
            f' {now}.csv')
        input('Program finished. Press Enter.')
    
    except Exception as e:
        log_error(str(e)+'\n')

if __name__ == '__main__':
    main()