import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from threading import Thread
# from concurrent.futures import ProcessPoolExecutor


def get_all_download_urls() -> None:
    with open('./data/url_for_site_of_picture.txt', 'r') as file:
        urls = file.read().split('\n')
    
    # Первый способ параллельного выполнения, который я пробовал
    thread_list = []
    for url in urls:
        try:
            thread_i = Thread(target=parse_url_for_download, args=(url,))
            thread_list.append(thread_i)
            thread_i.start()
        except Exception as ex:
            print(f'Error: {ex}')
    
    for th in thread_list:
        th.join()
    
    # Второй способ, параллельного выполнения, который я пробовал
    # Пробовал и этот вариант, но ту же работу сделал в два раза медленнее
    # with ProcessPoolExecutor() as executor:
    #     response = executor.map(parse_url_for_download, urls)
    


def parse_url_for_download(url) -> None:
    response = requests.get(url)
    if response.status_code != 404:
        soup = BeautifulSoup(response.text, 'lxml')
        download_url = 'https://zatavok.net' + \
                        soup.find('div', class_='image_data')\
                            .find('div', class_='block_down')\
                            .find('a').get('href')
                        
        with open('./data/download_urls.txt', 'a') as file:
            file.write(download_url + '\n')


def downloading_picture(url, name) -> None:
    headers = {
        'User-Agent': UserAgent().random
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 404:
            img = response.content
            
            with open(f'./data/imgs/{name}.jpg', 'wb') as file:
                file.write(img)
    except Exception as ex:
        print(f'Error: {ex}')


def main() -> None:
    get_all_download_urls()


if __name__ == "__main__":
    start_time = time.time()
    print('---' * 10 + '\nStart downloading...')
    main()
    print('Finish downloading...\n' + '---' * 10)
    finish_time = time.time()
    print(f'Download time = {finish_time - start_time}')
    