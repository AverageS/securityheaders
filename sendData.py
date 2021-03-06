# -*- coding: utf-8 -*-

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

try:
    es = elasticsearch.Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    es.indices.delete(index='headers')
    es.indices.create(index='headers', ignore=400, body=mapping)
except:
    es.indices.create(index='headers', ignore=400, body=mapping)


def trying_decorator(func):
    def wrapper(data, id, index='headers', doc_type='sub'):
        while True:
            try:
                func(data, id, index, doc_type)
                return
            except:
                time.sleep(10)
                pass
    return wrapper

@trying_decorator
def sendToElastic(data, id, index='headers', doc_type='sub'):
    es.index(index=index, doc_type=doc_type,id=id,body=data)
    logging.info('data sent')

