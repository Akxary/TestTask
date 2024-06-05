import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from db_models import agrmnt as db_agrmnt
from enum import Enum
from db_connect import engine


def init_db_data(db: Session):

    with engine.connect() as connection:
        cur = connection.cursor()
