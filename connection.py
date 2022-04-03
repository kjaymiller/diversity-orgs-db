import os

from elasticsearch import Elasticsearch

es_client = Elasticsearch(
    cloud_id = os.environ.get("ES_CLOUD_ID"),
    http_auth=[
        os.environ.get('ES_USER'),
        os.environ.get('ES_PWD'),
    ]
)
