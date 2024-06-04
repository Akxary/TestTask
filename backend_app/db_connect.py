from env_settings import settings as s
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
    user=s.postgres_user,
    password=s.postgres_password,
    host=s.postgres_host,
    port=s.db_port,
    db=s.postgres_db,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
