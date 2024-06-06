import numpy as np
import pandas as pd

from business_logic.date_operations import (
    calculate_payment_date_boundaries,
    get_period_number,
    calculate_stage_flg,
)


# ==================================================================
# ===================== Dataframe operations =======================
# ==================================================================


def get_agr_joined_base_retirement(
    agr_df: pd.DataFrame, retirement_df: pd.DataFrame
) -> pd.DataFrame:
    """
    :param agr_df: pd.DataFrame with columns [number, male, birth_date, retirement_years]
    :param retirement_df: pd.DataFrame with columns [agrmnt_number, base_retirement]
    :return: agr_df: pd.DataFrame with columns [number, male, birth_date, retirement_years, base_retirement]
    """
    merged = agr_df.merge(
        retirement_df, how="left", left_on=["number"], right_on=["agrmnt_number"]
    )
    merged = merged.drop(columns=["agrmnt_number"])
    return merged


def get_agr_retirement_boundaries(
    agr_df: pd.DataFrame,
    max_age: int,
) -> pd.DataFrame:
    """
    :param agr_df: pd.DataFrame with columns [number,birth_date, ..., retirement_years]
    :param max_age: int const (100 years)
    :return: agr_df: pd.DataFrame with columns [number,birth_date, ..., retirement_years, payment_start_dt, payment_end_dt]
    """

    agr_df["boundaries"] = agr_df.apply(
        lambda x: calculate_payment_date_boundaries(
            x["birth_date"], x["retirement_years"], max_age
        ),
        axis=1,
    )
    agr_df["payment_start_dt"] = (
        agr_df["boundaries"].apply(lambda x: x[0]).astype("datetime64[ns]")
    )  # [0]
    agr_df["payment_end_dt"] = (
        agr_df["boundaries"].apply(lambda x: x[1]).astype("datetime64[ns]")
    )  # [1]
    agr_df = agr_df.drop(columns=["boundaries"])
    return agr_df


def get_payment_period(agr_df: pd.DataFrame) -> pd.DataFrame:
    """
    :param agr_df: pd.DataFrame with columns [number, ..., payment_start_dt, payment_end_dt, report_date]
    :return: agr_df: pd.DataFrame with columns [number, ..., payment_start_dt, payment_end_dt, report_date, m, dor]
    """
    agr_with_stage = agr_df
    agr_with_stage["stage"] = agr_with_stage.apply(
        lambda df: calculate_stage_flg(
            df["report_date"], df["payment_start_dt"], df["payment_end_dt"]
        ),
        axis=1,
    )
    merge_list = []
    agr_with_stage_0 = agr_with_stage[agr_with_stage["stage"] == 0]
    if agr_with_stage_0.shape[0] > 0:
        agr_with_stage_0["m"] = 0
        agr_with_stage_0["dor"] = agr_with_stage_0["payment_start_dt"]
        merge_list.append(agr_with_stage_0)

    agr_with_stage_1 = agr_with_stage[agr_with_stage["stage"] == 1]
    if agr_with_stage_1.shape[0] > 0:
        agr_with_stage_1["m"] = agr_with_stage_1.apply(
            lambda df: get_period_number(df["report_date"], df["payment_start_dt"]),
            axis=1,
        )
        agr_with_stage_1["dor"] = agr_with_stage_1["report_date"]
        merge_list.append(agr_with_stage_1)

    agr_with_stage_2 = agr_with_stage[agr_with_stage["stage"] == 2]
    if agr_with_stage_2.shape[0] > 0:
        agr_with_stage_2["m"] = agr_with_stage_2.apply(
            lambda df: get_period_number(df["payment_end_dt"], df["payment_start_dt"]),
            axis=1,
        )
        agr_with_stage_2["dor"] = agr_with_stage_2["payment_end_dt"]
        merge_list.append(agr_with_stage_2)
    return pd.concat(merge_list, ignore_index=True)


def calculate_retirement_amount(
    agr_df: pd.DataFrame, coeff_value: float
) -> pd.DataFrame:
    """
    :param agr_df: pd.DataFrame with columns [number, ..., report_dt, base_retirement, m, dor]
    :param coeff_value: index coefficient of retirement
    :return: agr_df: pd.DataFrame with columns [number, ..., report_dt, base_retirement, m, dor, amount]
    """
    agr_df["amount"] = (
        np.power(1 + coeff_value, agr_df["m"]) * agr_df["base_retirement"]
    )
    return agr_df
