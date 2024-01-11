import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def parse_url_for_download(url) -> None:
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
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
    response = requests.get(url, headers=headers)
    if response.status_code != 404:
        img = response.content
        
        with open(f'./data/imgs/{name}.jpg', 'wb') as file:
            file.write(img)


def main() -> None:
    url = 'https://zastavok.net/download/66819/5120x2880/'
    downloading_picture(url=url, name='first_img')


if __name__ == "__main__":
    start_time = time.time()
    print('---' * 10 + '\nStart downloading...')
    main()
    print('Finish downloading...\n' + '---' * 10)
    finish_time = time.time()
    print(f'Download time = {finish_time - start_time}')
    