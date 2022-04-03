from fastapi import FastAPI
from connection import es_client
import os
import typing

app = FastAPI()

def get_es_results(query: dict) -> typing.Any:
    """
    Get results from Elasticsearch.
    
    """
    results = es_client.search(index=os.environ["DB_INDEX"], query=query)
    return results['hits']['hits']


@app.get("/")
async def hello():
    return {"message": "Hello World"}


@app.get("/orgs/all")
async def get_all_orgs():
    """Returns all orgs
    TODO: ADD RATE Limiting
    """
    return get_es_results({"query": {"match_all": {}}})


@app.get("/orgs/search")
async def search_orgs(q):
    """Returns all orgs"""

    query = {
        "simple_query_string": {
          "query": q,
          "fields": ["parent_organization", "location", "name"]
        }
        }

    return get_es_results(query)


@app.get("/orgs/by_geo/")
async def by_location(coords: str, distance: int=50, units: str="km"):
    """Returns all orgs near a given location"""

    query = {
        "geo_distance": {
          "distance": f"{distance}{units}",
          "location.location": coords
        }
    }

    return es_client.search(
            index=os.environ["DB_INDEX"],
            query=query)[
        "hits"
    ]["hits"]


@app.get("/orgs/by_parent/")
def get_orgs_by_parent(parent: str):
    """Returns all orgs near a given location"""

    query = {
        "match": {
            "parent": parent 
                }
            }

    return get_es_results(query)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
