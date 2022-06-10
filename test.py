from parse_functions import *

product = get_product_info('https://www.teplograd.ru/catalog/serie/kontrollery_salus_dlya_upravleniya_teplym_polom/salus_pl06')

keys = product.keys()


print(product['expandables'])