import time
import requests
from bs4 import BeautifulSoup


def fetch_url(main_url, url: str = None) -> None:
    try:
        response = requests.get(main_url).text
        soup = BeautifulSoup(response, 'lxml')
        photos_on_one_url = [main_url[:-1] + photo_url.find('a').get('href') 
                            for photo_url in soup.find_all('div', class_='short_prev')]
        
        with open('./data/url_for_site_of_picture.txt', 'a') as file:
            for picture_url in photos_on_one_url:
                file.write(picture_url + '\n')
                print(f'Writed: {picture_url}')
    except Exception as ex:
        print(f'Error: {ex}')
    

def main():
    main_url = 'https://zastavok.net/'
    fetch_url(main_url=main_url)


if __name__ == "__main__":
    start_time = time.time()
    main()
    finish_time = time.time()
    
    print(f'All time = {finish_time - start_time}')