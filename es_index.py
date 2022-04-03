from elasticsearch.helpers import bulk
import json

from connection import es_client

new_mappings = {
    "properties": {
        "location" : {
            "properties": {
                "location" : {"type": "geo_point"},
            }
        }
    }
}

src = "diversity_orgs_22020327"

with open('diversity-orgs.json') as j_file:
    data = json.load(j_file)

def index():
    """Index all documents with changes to mappings"""
    es_client.options(ignore_status=[404, 404]).indices.delete(index=src)
    es_client.indices.create(index=src, mappings=new_mappings)
    bulk(client=es_client, index=src, actions=data)

if __name__ == "__main__":
    index()