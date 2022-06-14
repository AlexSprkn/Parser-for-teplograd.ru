import all_categories
import choose_category

def main():
    user_choice = input('Choose mode:\n' +
        '0 - Download one category\n' +
        '1 - Download all categories\n' +
        'Mode: ')
    if user_choice[0].isdigit():
        user_choice = int(user_choice[0])
    if user_choice:
        all_categories.main()
    else:
        choose_category.main()

if __name__ == '__main__':
	main()