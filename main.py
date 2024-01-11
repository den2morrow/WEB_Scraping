import time
import requests
from bs4 import BeautifulSoup



def parse_url_for_download(url) -> None:
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    download_url = 'https://zatavok.net' + \
                    soup.find('div', class_='image_data')\
                        .find('div', class_='block_down')\
                        .find('a').get('href')
                    
    with open('./data/download_urls.txt', 'a') as file:
        file.write(download_url + '\n')


def main() -> None:
    parse_url_for_download(url='https://zastavok.net/funny/66615-kot_vzglyad_seryj_britanec_ispug.html')


if __name__ == "__main__":
    start_time = time.time()
    print('---' * 10 + '\nStart downloading...')
    main()
    print('Finish downloading...\n' + '---' * 10)
    finish_time = time.time()
    print(f'Download time = {finish_time - start_time}')
    