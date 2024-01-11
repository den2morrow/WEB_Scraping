import time


def main() -> None:
    pass


if __name__ == "__main__":
    start_time = time.time()
    print('---' * 10 + '\nStart downloading...')
    main()
    print('Finish downloading...\n' + '---' * 10)
    finish_time = time.time()
    print(f'Download time = {finish_time - start_time}')
    