import elasticsearch
import time
import logging


mapping = {
    "mappings": {
        "_default_": {
            "dynamic_templates": [{
                "message_field": {
                    "mapping": {
                        "index": "analyzed",
                        "omit_norms": True,
                        "type": "string",
                        "fields": {
                            "raw": {
                                "ignore_above": 1024,
                                "index": "not_analyzed",
                                "type": "string"
                            }
                        }
                    },
                    "match_mapping_type": "string",
                    "match": "message"
                }
            }, {
                "string_fields": {
                    "mapping": {
                        "index": "analyzed",
                        "omit_norms": True,
                        "type": "string",
                        "fields": {
                            "raw": {
                                "ignore_above": 1024,
                                "index": "not_analyzed",
                                "type": "string"
                            }
                        }
                    },
                    "match_mapping_type": "string",
                    "match": "*"
                }
            }
            ],
            "properties": {
                "latestRefresh": {"type": "date"},
            }
        }
    }
}



def sendToElastic(data, id, index='hosts', doc_type='sub'):
    while True:
        try:
            es = elasticsearch.Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
            break
        except:
            pass
        es.indices.create(index='hosts', ignore=400, body=mapping)
    for i in range(10):
        try:
            es.index(index=index, doc_type=doc_type,id=id,body=data)
        except:
            time.sleep(10)
        else:
            return
    logging.error('Could not send data to elastic')

