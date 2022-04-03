from multiprocessing import parent_process
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    create_engine,
    ForeignKey,
    MetaData,
)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    region = Column(String)
    country = Column(String)
    location = Column(String)

    def __repr__(self):
        return f'<Location(name={self.name}, region={self.region}, country={self.country}, location={self.location})>'

class DiversityFocus(Base):
    __tablename__ = 'diversity_focus'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'<DiversityFocus(name={self.name})>'


class TechnologyFocus(Base):
    __tablename__ = 'technology_focus'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'<TechnologyFocus(name={self.name})>'

class ParentOrganization(Base):
    __tablename__ = 'parent_organization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url =  Column(String)

organization_technology_focus_association = Table(
    'organization_technology_focus', Base.metadata,
    Column('organization', ForeignKey('organization.id'), primary_key=True),
    Column('technology_focus', ForeignKey('technology_focus.id'), primary_key=True),
)

organization_diversity_focus_association = Table(
    'organization_diversity_focus', Base.metadata,
    Column('organzation_id', ForeignKey('organization.id'), primary_key=True),
    Column('diversity_focus_id', ForeignKey('diversity_focus.id'), primary_key=True)
)

class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_organization = Column(Integer, ForeignKey('parent_organization.id'))
    url = Column(String)
    location_id = Column(Integer, ForeignKey('location.id'))
    diversity_focuses = relationship('DiversityFocus', secondary=organization_diversity_focus_association)
    technology_focuses = relationship('TechnologyFocus', secondary=organization_technology_focus_association)



engine = create_engine('sqlite:///diversity-organizations.db', future=True)
metadata = Base.metadata