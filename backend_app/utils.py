from enum import Enum
import pandas as pd
from pathlib import Path


input_data_path = Path("./Данные.xlsx")


class XlsxSheet(Enum):
    agrs = "Договоры участников"
    retirements = "Суммы пенсий"
    params = "Параметры расчета"


def get_input_dfs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    xlsx_file = pd.ExcelFile(input_data_path)
    # read from file
    agr_df = pd.read_excel(xlsx_file, sheet_name=XlsxSheet.agrs.value)
    agr_df = agr_df.rename(
        columns={
            "Номер договора": "number",
            "Пол участника": "male",
            "Дата рождения участника": "birth_date",
            "Пенсионный возраст": "retirement_years",
        }
    )
    retirements_df = pd.read_excel(xlsx_file, sheet_name=XlsxSheet.retirements.value)
    retirements_df = retirements_df.rename(
        columns={
            "Номер договора": "agrmnt_number",
            "Установленный размер пенсии": "base_retirement",
        }
    )
    params_df = pd.read_excel(xlsx_file, sheet_name=XlsxSheet.params.value, header=None)
    params_df.columns = ["param", "value"]

    return agr_df, retirements_df, params_df


if __name__ == "__main__":
    df1, df2, df3 = get_input_dfs()
    print("agr_df")
    print("-" * 100)
    print(df1)
    print("retirement_df")
    print("-" * 100)
    print(df2)
    print("params_df")
    print("-" * 100)
    print(df3)
