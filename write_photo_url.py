import time
import requests
from bs4 import BeautifulSoup

from typing import Iterator
from concurrent.futures import ProcessPoolExecutor


def fetch_url(url: str) -> None:
    try:
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'lxml')
        photos_on_one_url = [url[:-1] + photo_url.find('a').get('href') 
                            for photo_url in soup.find_all('div', class_='short_prev')]
        
        with open('./data/url_for_site_of_picture.txt', 'a') as file:
            for picture_url in photos_on_one_url:
                file.write(picture_url + '\n')
                print(f'Writed: {picture_url}')
    except Exception as ex:
        print(f'Error: {ex}')


def get_all_urls(url_list: list[str]) -> Iterator[None]:
    with ProcessPoolExecutor() as executor:
        response = executor.map(fetch_url, url_list)
    return response


def main() -> None:
    main_url = 'https://zastavok.net/'
    htmlik = requests.get(main_url).text
    soup = BeautifulSoup(htmlik, 'lxml')
    num_urls = soup.find('div', class_='ruler').find_all('a')[-2].text
    urls = [main_url for _ in range(int(num_urls))]
    
    print('--' * 49 + '\nStart writting urls...')
    
    start_download = int(input('Введите с какой фотографии начать скачивание (введите целое число): '))
    end_download = int(input('Введите до какой фотографии скачивать (введите целое число): '))
    get_all_urls(urls[start_download:end_download])
    
    print('--' * 49 + '\nFinish writting urls...')
    

if __name__ == "__main__":
    start_time = time.time()
    main()
    finish_time = time.time()
    
    print(f'All time = {finish_time - start_time}')