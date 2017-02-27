from checkUrls import getHeaders, checkHeaders
from sendData import sendToElastic
import time
import multiprocessing as multiprocessing
import logging


def scanUrl(tuple):
    try:
        url, index = tuple
        headers = getHeaders(url)
        if headers is None:
            return url
        grade = checkHeaders(headers)
        data = {
           'host_url': url,
           'raw_headers': headers,
           'headers_grade': grade,
           'presented_headers': ' '.join([key.replace('-', 'I') for key, value in headers.items() if 'MISSING' not in value ]),
           'missing_headers': ' '.join([key.replace('-', 'I') for key, value in headers.items() if 'MISSING' in value ]),
           'latestRefresh': int(round(time.time() * 1000))
        }
        logging.info(str(data))

        sendToElastic(data, id=index)
        return ''
    except Exception as e:
        logging.error('Something went very wrong with url: ' + url)
        return url


def launchScan(url_file):
    with open(url_file) as fp:
        urls_index_tuple = [(t.replace('\n', ''), index) for index, t in enumerate(fp.readlines())]
    p = multiprocessing.Pool(processes=4, maxtasksperchild=1)
    errors = list(p.map(scanUrl, urls_index_tuple, 15))
    with open('corrupted_urls', 'w') as fp:
        [fp.writelines(x + '\n') for x in errors]
    p.close()

if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    while True:
        launchScan('/usr/share/all_domains')
        time.sleep(86400)
