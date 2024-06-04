import pandas as pd

from business_logic.date_operations import calculate_payment_date_boundaries


# ==================================================================
# ===================== Date operations ============================
# ==================================================================


def get_agr_joined_base_retirement(
    agr_df: pd.DataFrame, retirement_df: pd.DataFrame
) -> pd.DataFrame:
    """
    :param agr_df: [number, male, birth_date, retirement_years]
    :param retirement_df: [agrmnt_number, base_retirement]
    :return: agr_df: [number, male, birth_date, retirement_years, base_retirement]
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
    :param agr_df: [number, male, birth_date, retirement_years, base_retirement]
    :param max_age: const (100 years)
    :return: agr_df: [number, male, birth_date, retirement_years, base_retirement, payment_start_dt, payment_end_dt]
    """
    agr_df["boundaries"] = agr_df.apply(
        lambda x: calculate_payment_date_boundaries(
            x["birth_date"], x["retirement_date"], max_age
        ),
        axis=1,
    )
    agr_df["payment_start_dt"] = agr_df["boundaries"].apply(lambda x: x[0])
    agr_df["payment_end_dt"] = agr_df["boundaries"].apply(lambda x: x[1])
    agr_df = agr_df.drop(columns=["boundaries"])
    return agr_df
