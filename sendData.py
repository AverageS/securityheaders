import elasticsearch

es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])

def sendToElastic(data, id, index='hosts', doc_type='sub'):
    es.index(index=index, doc_type=doc_type,id=id,body=data)

if __name__ == '__main__':
    for i in 'some string'.split():
        sendToElastic({'fiel': i})