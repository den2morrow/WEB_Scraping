from concurrent.futures import ProcessPoolExecutor
import time
from typing import Iterator
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from threading import Thread


def get_all_download_urls() -> None:
    with open('./data/url_for_site_of_picture.txt', 'r') as file:
        urls = file.read().split('\n')
    

    thread_list = []
    for url in urls[:-1]:
        try:
            thread_i = Thread(target=parse_url_for_download, args=(url,))
            thread_list.append(thread_i)
            thread_i.start()
        except Exception as ex:
            print(f'Error: {ex}')
    
    [th.join() for th in thread_list]
    
    with open('./data/download_urls.txt', 'r') as file:
        all_download_urls = file.read().split('\n')[:-1]
    return all_download_urls


def parse_url_for_download(url: str) -> None:
    response = requests.get(url)
    if response.status_code != 404:
        soup = BeautifulSoup(response.text, 'lxml')
        download_url = 'https://zatavok.net' + \
                        soup.find('div', class_='image_data')\
                            .find('div', class_='block_down')\
                            .find('a').get('href')
                        
        with open('./data/download_urls.txt', 'a') as file:
            file.write(download_url + '\n')


def downloading_picture(url: str) -> None:
    headers = {
        'User-Agent': UserAgent().random
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 404:
            img = response.content
            name = url.split('/')[-3]
            
            with open(f'./data/imgs/{name}.jpg', 'wb') as file:
                file.write(img)
    except Exception as ex:
        print(f'Error: {ex}')


def main() -> None:
    download_urls = get_all_download_urls()
    for url in download_urls:
        downloading_picture(url)


if __name__ == "__main__":
    start_time = time.time()
    print('---' * 10 + '\nStart downloading...')
    main()
    print('Finish downloading...\n' + '---' * 10)
    finish_time = time.time()
    print(f'Download time = {finish_time - start_time}')
    