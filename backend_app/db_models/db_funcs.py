import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from db_models import agrmnt as db_agrmnt
from enum import Enum
from db_connect import engine


def init_db_data(db: Session):
    class XlsxSheet(Enum):
        agrmnts = "Договоры участников"
        retirements = "Суммы пенсий"

    xlsx_file = pd.ExcelFile("Данные.xlsx")
    # read from file
    agrmnts_df = pd.read_excel(xlsx_file, sheet_name=XlsxSheet.agrmnts.value)
    retirements_df = pd.read_excel(xlsx_file, sheet_name=XlsxSheet.retirements.value)

    with engine.connect() as connection:
        cur = connection.cursor()