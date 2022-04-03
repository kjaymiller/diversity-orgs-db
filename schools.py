"""Uploads the US Dept of Education Data into an Elasticsearch instance"""

import json
import pathlib
from csv import DictReader
import typing

from elasticsearch.helpers import bulk

from connection import cloud_client as client


def load_convertor(
    coverter: pathlib.Path,
) -> typing.Generator[dict[str, typing.Any], None, None]:
    """Loads a convertor file"""
    with open(coverter, "r") as f:
        return json.loads(f.read())


convertors = {
    "CONTROL": load_convertor("translations/control.json"),
    "ST_FIPS": load_convertor("translations/st_fips.json"),
}


def gen_school_data(row) -> dict[str, typing.Any]:
    """Generates a dictionary of school data from the CSV file"""

    potential_taglist = [
        "HBCU",
        "PBI",
        "ANNHI",
        "TRIBAL",
        "AANAPII",
        "HSI",
        "NANTI",
        "MENONLY",
        "WOMENONLY",
    ]

    return {
        "name": row["INSTNM"],
        "city": row["CITY"],
        "state": row["STABBR"],
        "zip": row["ZIP"],
        "debt_median": row["DEBT_MDN"],
        "location": {
            "lat": row["LATITUDE"],
            "lon": row["LONGITUDE"],
        },
        "tags": [k for k in potential_taglist if row[k] == "1"],
        "main_campus": row['MAIN'] == "1",
    }


def gen_school_bulk() -> typing.Generator[dict[str, typing.Any], None, None]:

    with open("schools.csv", "r") as f:
        reader = DictReader(f)

        for row in reader:
            yield gen_school_data(row)


mappings = {
    "properties": {
        "location": {
            "type": "geo_point",
            "ignore_malformed": True,
        },
        "debt_median": {
            "type": "float",
            "ignore_malformed": True,
        },
    }
}
client.indices.delete(index="schools", ignore=400)
client.indices.create(index="schools", ignore=400, mappings=mappings)
bulk(client=client, actions=gen_school_bulk(), index="schools")
