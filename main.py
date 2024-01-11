from write_photo_url import main as writting_photo_urls
from download import main as download_all_photo


def main() -> None:
    writting_photo_urls()
    download_all_photo()


if __name__ == "__main__":
    main()