from enum import Enum
from io import BytesIO
from typing import BinaryIO

import pandas as pd
from pathlib import Path


input_data_path = Path("./Данные.xlsx")


class XlsxSheet(Enum):
    agrs = "Договоры участников"
    retirements = "Суммы пенсий"
    params = "Параметры расчета"


class AgrRenameMapping(Enum):
    number = "Номер договора"
    male = "Пол участника"
    birth_date = "Дата рождения участника"
    retirement_years = "Пенсионный возраст"


class AgrDtype(Enum):
    number = "str"
    male = "str"
    birth_date = "datetime64[ns]"
    retirement_years = "int64"


class RetirementRenameMapping(Enum):
    agrmnt_number = "Номер договора"
    base_retirement = "Установленный размер пенсии"


class RetirementDtype(Enum):
    agrmnt_number = "str"
    base_retirement = "float64"


def get_input_dfs(
    input_data: str | Path | bytes | BinaryIO,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    xlsx_file = pd.ExcelFile(input_data)
    # read from file
    agr_df = pd.read_excel(xlsx_file, sheet_name=XlsxSheet.agrs.value)
    agr_df = agr_df.rename(columns={e.value: e.name for e in AgrRenameMapping})
    for e in AgrDtype:
        agr_df[e.name] = agr_df[e.name].astype(e.value)

    retirements_df = pd.read_excel(xlsx_file, sheet_name=XlsxSheet.retirements.value)
    retirements_df = retirements_df.rename(
        columns={e.value: e.name for e in RetirementRenameMapping}
    )
    for e in RetirementDtype:
        retirements_df[e.name] = retirements_df[e.name].astype(e.value)

    params_df = pd.read_excel(xlsx_file, sheet_name=XlsxSheet.params.value, header=None)
    params_df.columns = ["param", "value"]

    return agr_df, retirements_df, params_df


if __name__ == "__main__":
    with open(input_data_path, mode="rb") as f:
        # input_data_path.open(mode="rb"))
        df1, df2, df3 = get_input_dfs(f)
    print("agr_df")
    print("-" * 100)
    print(df1)
    print("=" * 100)
    print("retirement_df")
    print("-" * 100)
    print(df2)
    print("=" * 100)
    print("params_df")
    print("-" * 100)
    print(df3)
