import pandas as pd
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import Engine
from db_models.agrmnt import Agrmnt, BaseRetirement, Payment
from sqlalchemy import func
from db_models import agrmnt as db_agrmnt
from enum import Enum
from db_connect import engine, Base


def init_db_data(db: Session):

    with engine.connect() as connection:
        cur = connection.cursor()


def recreate_db_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def insert_agrmnt(db: Session, agr_df: pd.DataFrame) -> int:
    list_to_write = agr_df.to_dict(orient="records")
    db.add_all(map(lambda row: Agrmnt(**row), list_to_write))
    db.commit()
    return db.query(Agrmnt).count()


def insert_base_retirement(db: Session, base_retirement_df: pd.DataFrame) -> int:
    list_to_write = base_retirement_df.to_dict(orient="records")
    db.add_all(map(lambda row: BaseRetirement(**row), list_to_write))
    db.commit()
    return db.query(BaseRetirement).count()
