from typing import List, Type

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


def recreate_db_tables(db: Session):
    print(Base.metadata.tables)
    Base.metadata.drop_all(bind=db.bind)
    Base.metadata.create_all(bind=db.bind)
    db.commit()


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


def insert_payment(db: Session, payment_df: pd.DataFrame) -> int:
    list_to_write = payment_df.to_dict(orient="records")
    db.add_all(map(lambda row: Payment(**row), list_to_write))
    db.commit()
    return db.query(Payment).count()


def get_agrmnt(db: Session) -> list[Type[Agrmnt]]:
    return db.query(Agrmnt).all()


def get_agrmnt_pd(db: Session) -> pd.DataFrame:
    return pd.read_sql_table(Agrmnt.__tablename__, db.bind, index_col="id")


def get_base_retirement(db: Session) -> list[Type[BaseRetirement]]:
    return db.query(BaseRetirement).all()


def get_base_retirement_pd(db: Session) -> pd.DataFrame:
    return pd.read_sql_table(BaseRetirement.__tablename__, db.bind, index_col="id")


def get_payments(db: Session) -> list[Type[Payment]]:
    return db.query(Payment).all()


def get_payments_pd(db: Session) -> pd.DataFrame:
    return pd.read_sql_table(Payment.__tablename__, db.bind, index_col="id")
