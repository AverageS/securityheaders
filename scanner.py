from checkUrls import getHeaders, checkHeaders
from sendData import sendToElastic
import time
import logging


def launchScan(url_file):
    with open(url_file) as fp:
        urls = [t.replace('\n', '') for t in fp.readlines()]
    for index, url in enumerate(urls):
        headers = getHeaders(url)
        if headers is None:
            logging.error(' '.join([url, 'could not get']))
            continue
        grade = checkHeaders(headers)
        data = {
            'host_url': url,
            'raw_headers': headers,
            'headers_grade': grade,
            'latestRefresh': int(round(time.time() * 1000))
        }
        logging.info(' '.join([url, 'sent to elastic']))
        sendToElastic(data, id=index)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
    launchScan('domains')
