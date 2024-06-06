import unittest
from datetime import date

import pandas as pd

from business_logic.pd_df_operations import (
    get_agr_joined_base_retirement,
    get_agr_retirement_boundaries,
    get_payment_period,
    calculate_retirement_amount,
)


class PdDfOperationsTest(unittest.TestCase):

    # warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

    def df_output(self, exp, ans, join_key: list):
        cols = list(filter(lambda x: x not in set(join_key), exp.columns))
        merged = pd.merge(ans, exp, on=join_key, how="outer", suffixes=("_l", "_r"))
        cnt = merged.shape[0]
        for col in cols:
            merged[col + "_eq"] = merged[col + "_l"] == merged[col + "_r"]
            act = int(merged[col + "_eq"].sum())
            flg = act == cnt
            print(
                f"[{'passed' if flg else 'failed'}] for {col=} expected eq: {cnt} actual: {act}"
            )
            if not flg:
                print(merged[join_key + [col + "_l", col + "_r"]])
            self.assertEqual(cnt, act)

    def test_get_agr_joined_base_retirement(self):
        agr_columns = ["number", "male", "birth_date", "retirement_years"]
        ret_columns = ["agrmnt_number", "base_retirement"]
        agr = pd.DataFrame([[10001, "Y", "1963-07-16", 58]], columns=agr_columns)
        ret = pd.DataFrame([[10001, 3000]], columns=ret_columns)
        exp = pd.DataFrame(
            [[10001, "Y", "1963-07-16", 58, 3000]],
            columns=agr_columns + ret_columns[1:],
        )
        ans = get_agr_joined_base_retirement(agr, ret)
        self.df_output(exp, ans, ["number"])

    def test_get_agr_retirement_boundaries(self):
        agr_columns = ["number", "birth_date", "retirement_years"]
        agr_res_columns = agr_columns + ["payment_start_dt", "payment_end_dt"]
        agr = pd.DataFrame([[10001, date(2023, 2, 22), 1]], columns=agr_columns)
        exp = pd.DataFrame(
            [[10001, date(2023, 2, 22), 1, date(2024, 2, 29), date(2025, 2, 28)]],
            columns=agr_res_columns,
        )
        ans = get_agr_retirement_boundaries(agr, 2)
        self.df_output(exp, ans, ["number"])

    def test_get_payment_period(self):
        agr_columns = ["number", "payment_start_dt", "payment_end_dt", "report_date"]
        agr_res_columns = agr_columns + ["m", "dor"]
        agr = pd.DataFrame(
            [
                [1001, date(2020, 2, 29), date(2024, 2, 29), date(2019, 2, 28)],
                [1002, date(2020, 2, 29), date(2024, 2, 29), date(2025, 2, 28)],
                [1003, date(2020, 2, 29), date(2024, 2, 29), date(2023, 2, 28)],
            ],
            columns=agr_columns,
        )
        exp = pd.DataFrame(
            [
                [
                    1001,
                    date(2020, 2, 29),
                    date(2024, 2, 29),
                    date(2019, 2, 28),
                    0,
                    date(2020, 2, 29),
                ],
                [
                    1002,
                    date(2020, 2, 29),
                    date(2024, 2, 29),
                    date(2025, 2, 28),
                    4 * 12,
                    date(2024, 2, 29),
                ],
                [
                    1003,
                    date(2020, 2, 29),
                    date(2024, 2, 29),
                    date(2023, 2, 28),
                    3 * 12,
                    date(2023, 2, 28),
                ],
            ],
            columns=agr_res_columns,
        )
        ans = get_payment_period(agr)
        self.df_output(exp, ans, join_key=["number"])

    def test_calculate_retirement_amount(self):
        agr_columns = ["number", "base_retirement", "m"]
        agr_res_columns = agr_columns + ["amount"]
        agr = pd.DataFrame([[10001, 2.0, 4], [10002, 2.0, 0]], columns=agr_columns)
        exp = pd.DataFrame(
            [[10001, 2.0, 4, 32.0], [10002, 2.0, 0, 2.0]], columns=agr_res_columns
        )
        ans = calculate_retirement_amount(agr, 1.0)
        self.df_output(exp, ans, ["number"])
