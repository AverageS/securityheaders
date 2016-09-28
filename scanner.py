from checkUrls import getHeaders, checkHeaders
#from sendData import sendToElastic
import time
import multiprocessing.dummy as multiprocessing
from contextlib import closing
import logging


def scanUrl(url):
    try:
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
        #logging.info(' '.join([url, 'sent to elastic']))
        #sendToElastic(data, id=index)
        return ''
    except Exception as e:
        print('Something went very wrong with url: ' + url)
        return url

def launchScan(url_file):
    while True:
        with open(url_file) as fp:
            urls = [t.replace('\n', '') for t in fp.readlines()]
        formatted_urls = ['https://' + url if "http" not in url else url for url in urls]
        #urls = formatted_urls
        i = 0
        errors = []
        simul_scans = 30

        while i < len(urls):
            with closing(multiprocessing.Pool(simul_scans)) as p:
                errors.extend(list(p.map(scanUrl, urls[i:i + 15])))
                i += simul_scans
                print('yoba')

        ans = [x for x in errors if x != '']
        print(ans)
        print(len(ans))

        '''
        counter = 0
        error_urls = []
        for index, url in enumerate(urls):
            try:
                scanUrl(url)
                counter += 1
            except:
                error_urls.append(url)
        '''
        #logging.info('ALL %d \nSUCCESFULL %d', index, counter)
        #print(error_urls)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')
    launchScan('all_domains')
