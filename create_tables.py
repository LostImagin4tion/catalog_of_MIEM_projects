from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from config import settings


# creating engine
db = declarative_base()
engine = create_engine(settings.DB_PATH, pool_size=1000)


# table with base project info
class ProjectBasic(db):
    __tablename__ = 'projects_basic_info'

    id = Column(Integer, primary_key=True, unique=True)
    number = Column(Integer)
    name = Column(String(200))
    head = Column(String(200))
    vacancies = Column(Integer)
    status = Column(String(200))
    type = Column(String(200))
    image = Column(String(200))


# table with project details
class ProjectDetails(db):
    __tablename__ = 'projects_details'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Text)
    team = Column(Text)
    vacancies = Column(Text)
    link = Column(Text)
    wiki_link = Column(Text)
    zulip_link = Column(Text)
    email = Column(Text)
    target = Column(Text)
    annotation = Column(Text)
    results = Column(Text)
    competency = Column(Text)
    resources = Column(Text)
    control = Column(Text)
    result_form = Column(Text)
    background = Column(Text)
    customer = Column(Text)
    industry = Column(Text)
    organization = Column(Text)


# creating database and tables
def create_tables(engine: Engine) -> None:
    print(f'Database exists: {database_exists(engine.url)}')
    if not database_exists(settings.DB_PATH):
        create_database(engine.url)
        print(f'Database created: {database_exists(engine.url)}')
    db.metadata.create_all(engine)


# creating session
def get_session(engine: Engine) -> Session:
    return sessionmaker(bind=engine, autoflush=False)()


# Dropping the tables
def delete_tables() -> None:
    ProjectBasic.__table__.drop(engine)
    ProjectDetails.__table__.drop(engine)


# Deleting all tables' content
def truncate_tables() -> None:
    engine.execute('TRUNCATE TABLE projects_basic_info')
    engine.execute('TRUNCATE TABLE projects_details')


if __name__ == '__main__':
    create_tables(engine)
