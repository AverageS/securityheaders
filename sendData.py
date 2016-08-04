import elasticsearch
import time
import logging

es = elasticsearch.Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

def sendToElastic(data, id, index='hosts', doc_type='sub'):
    for i in range(10):
        try:
            es.index(index=index, doc_type=doc_type,id=id,body=data)
        except:
            time.sleep(10)
        else:
            return
    logging.error('Could not send data to elastic')

if __name__ == '__main__':
    for i in 'some string'.split():
        sendToElastic({'fiel': i})