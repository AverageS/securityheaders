from checkUrls import getHeadersAndCheck
import multiprocessing
import logging


def launchScan(url_file, proc_count=5):
    with open(url_file) as fp:
        urls = fp.readlines()
    for url in urls:
        getHeadersAndCheck(url)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
    launchScan('domains')
