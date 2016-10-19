from checkUrls import getHeaders, checkHeaders
from sendData import sendToElastic
import time
import multiprocessing as multiprocessing
import logging


def scanUrl(tuple):
    try:
        url,index = tuple
        headers = getHeaders(url)
        if headers is None:
            return url
        grade = checkHeaders(headers)
        data = {
            'host_url': url,
           'raw_headers': headers,
           'headers_grade': grade,
           'latestRefresh': int(round(time.time() * 1000))
        }
        logging.info(' '.join([url, 'sent to elastic']))
        sendToElastic(data, id=index)
        return ''
    except Exception as e:
        print('Something went very wrong with url: ' + url)
        return url

def launchScan(url_file):
    while True:
        with open(url_file) as fp:
            urls_index_tuple = [(t.replace('\n', ''), index) for index, t in enumerate(fp.readlines())]
        p = multiprocessing.Pool(processes=15, maxtasksperchild=1)
        errors = list(p.map(scanUrl, urls_index_tuple, 15))
        ans = [x for x in errors if x != '']
        print(ans)
        not_ans = [x[0] for x in urls_index_tuple if x[0] not in ans ]
        for x in not_ans:
            print(x + '\n')
        return


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')
    launchScan('/usr/share/all_domains')
