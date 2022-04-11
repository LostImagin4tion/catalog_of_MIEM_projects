from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from config import settings


# creating engine
db = declarative_base()
engine = create_engine(settings.DB_PATH, pool_size=1000)


# table with base project info
class ProjectBasic(db):
    __tablename__ = 'basic_info'

    id = Column(Integer, primary_key=True, unique=True)
    number = Column(Integer)
    name = Column(String)
    head = Column(String)
    workers_amount = Column(Integer)
    vacancies = Column(Integer)
    status = Column(String)
    image = Column(String)


# table with project details
class ProjectDetails(db):
    __tablename__ = 'details'

    id = Column(Integer, primary_key=True, unique=True)
    number = Column(Integer, unique=True)
    name = Column(String)
    head = Column(String)
    team = Column(String)
    status = Column(String)
    target = Column(String)
    annotation = Column(String)
    results = Column(String)
    competency = Column(String)
    resources = Column(String)
    control = Column(String)
    result_form = Column(String)
    background = Column(String)
    customer = Column(String)
    industry = Column(String)
    organization = Column(String)
    vacancies = Column(String)
    years = Column(String)
    image = Column(String)


# creating tables
def create_tables(engine: Engine) -> None:
    db.metadata.create_all(engine)


# creating session
def get_session(engine: Engine) -> Session:
    return sessionmaker(bind=engine)()


# Dropping the tables
def delete_tables():
    ProjectBasic.__table__.drop(engine)
    ProjectDetails.__table__.drop(engine)


if __name__ == '__main__':
    create_tables(engine)
