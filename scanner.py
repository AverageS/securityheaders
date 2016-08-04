from checkUrls import getHeaders, checkHeaders
from sendData import sendToElastic
import time
import logging


def scanUrl(url, index):
    try:
        headers = getHeaders(url)
        if headers is None:
            logging.error(' '.join([url, 'could not get']))
            return
        grade = checkHeaders(headers)
        data = {
            'host_url': url,
            'raw_headers': headers,
            'headers_grade': grade,
            'latestRefresh': int(round(time.time() * 1000))
        }
        logging.info(' '.join([url, 'sent to elastic']))
        sendToElastic(data, id=index)
    except:
        logging.error('Something went very wrong with url: ' + url)

def launchScan(url_file):
    while True:
        with open(url_file) as fp:
            urls = [t.replace('\n', '') for t in fp.readlines()]
        for index, url in enumerate(urls):
            scanUrl(url, index)


if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/sec_header_scan.log',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
    launchScan('/usr/share/all_domains')
