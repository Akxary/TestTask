from pydantic import BaseModel, Field
from datetime import date


class CalcParams(BaseModel):
    report_date: date = Field(default=date(2024,1,31))
    coeff_value: float = Field(default=0.1)
    max_age: int = Field(default=100)


class RetirementBase(BaseModel):
    agrmnt_number: str
    report_date: date
    amount: float


class RetirementFull(RetirementBase):
    payment_start_dt: date
    payment_end_dt: date
    date_of_retirement: date
