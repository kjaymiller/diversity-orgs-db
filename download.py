from connection import es_client
from pathlib import Path
import json
import typer

match = {"match_all": {}}
result = es_client.search(index="diversity-orgs", query=match, size=2000)

Path('diversity-orgs.json').write_text(json.dumps([x['_source'] for x in result['hits']['hits']], indent=2))
