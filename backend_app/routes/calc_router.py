import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import get_db
from db_models.db_funcs import get_agrmnt_pd, get_base_retirement_pd, insert_payment
from response_models.models import CalcParams, RetirementFull
from business_logic.pd_df_operations import (
    get_agr_joined_base_retirement,
    get_agr_retirement_boundaries,
    get_payment_period,
    calculate_retirement_amount,
)

router = APIRouter(prefix="/calc", tags=["api", "calc"])


@router.post("/", response_model=list[RetirementFull])
async def calc_retirement(calc_params: CalcParams, db: Session = Depends(get_db)):
    # get base dfs
    try:
        agr_df = get_agrmnt_pd(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        ret_df = get_base_retirement_pd(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # transform dfs
    agr_df = get_agr_joined_base_retirement(agr_df, ret_df)
    agr_df = get_agr_retirement_boundaries(agr_df, calc_params.max_age)
    agr_df["report_date"] = calc_params.report_date
    agr_df["report_date"] = agr_df["report_date"].astype("datetime64[ns]")
    # print(agr_df.dtypes)
    agr_df = get_payment_period(agr_df)
    agr_df = calculate_retirement_amount(agr_df, calc_params.coeff_value)

    # insert result
    agr_df = agr_df.rename(
        columns={"number": "agrmnt_number", "dor": "date_of_retirement"}
    )
    agr_df = agr_df[
        [
            "agrmnt_number",
            "payment_start_dt",
            "payment_end_dt",
            "date_of_retirement",
            "report_date",
            "amount",
        ]
    ]
    payment_df = agr_df[["agrmnt_number", "report_date", "amount"]]

    try:
        insert_payment(db, payment_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    list_to_response = agr_df.to_dict(orient="records")
    return list(map(lambda row: RetirementFull(**row), list_to_response))
