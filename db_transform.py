import logging
import json
from sqlalchemy.orm import sessionmaker
from db import (
    engine,
    Organization,
    Location,
    TechnologyFocus,
    DiversityFocus,
    ParentOrganization,
    metadata,
)

Session = sessionmaker(bind=engine)


def get_or_create(session, model, **kwargs):
    """
    Get or create a model instance.
    """

    instance = session.query(model).filter_by(**kwargs).first()

    if instance:
        logging.debug(f"{instance} already exists")
        return instance

    else:
        instance = model(**kwargs)
        logging.debug(f"Creating {instance}")
        session.add(instance)
        return instance


def column_build(json_file: str) -> None:
    """
    Builds a list of column names from a json file.
    """

    with open(json_file, "r") as f:
        data = json.load(f)

    with Session() as session:
        for row in data:
            fields = ('name','url', 'logo')
            org = get_or_create(
                session,
                Organization,
                **{k:v for k, v in row.items() if k in fields and v},
            )

            if "location" in row:
                fields=("name", "region", "country", "location")
                org.location_id = get_or_create(
                        session=session,
                        model=Location,
                        **{k:v for k, v in row['location'].items() if k in fields and v},
                    ).id

            if 'diversity_focus' in row:
                org.diversity_focuses = [get_or_create(
                    session=session,
                    model=DiversityFocus,
                    name=diversity_focus,
                ) for diversity_focus in row.get('diversity_focus', [])]

            if 'technology_focus' in row:
                org.technology_focuses = [get_or_create(
                    session=session,
                    model=TechnologyFocus,
                    name=technology_focus,
                ) for technology_focus in row.get('technology_focus', [])]

            if 'parent_organization' in row:
                org.parent_organization = get_or_create(
                    session=session,
                    model=ParentOrganization,
                    name=row['parent_organization'],
                ).id

        session.commit()

if __name__ == "__main__":
    metadata.create_all(engine)
    column_build("diversity-orgs.json")