from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from db_connect import get_db
from db_models.db_funcs import get_payments_pd

router = APIRouter(prefix="/result", tags=["result"])


@router.get("/payments")  # , response_model=list[RetirementBase]
async def get_result(db: Session = Depends(get_db)):
    payments_df = get_payments_pd(db).drop_duplicates()
    # list_to_response = payments_df.to_dict("records")
    # return list(map(lambda row: RetirementBase(**row), list_to_response))
    payments_df = payments_df[["agrmnt_number", "report_date", "amount"]].rename(
        columns={
            "agrmnt_number": "Номер договора",
            "report_date": "Дата платежа",
            "amount": "Размер пенсии",
        }
    )
    payments_df.to_excel("payments.xlsx", index=False)
    headers = {
        "Content-Disposition": f"attachment; filename=payments.xlsx",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control_Allow-Methods": "POST, GET, OPTIONS",
    }
    return FileResponse(
        "payments.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
