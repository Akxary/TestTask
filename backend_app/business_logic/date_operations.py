import calendar
import datetime


def get_last_day_of_month(date: datetime.date) -> datetime.date:
    # next_month_date = date.replace(day=28) + datetime.timedelta(days=4)
    # return next_month_date - datetime.timedelta(days=next_month_date.day)
    return datetime.date(
        year=date.year,
        month=date.month,
        day=calendar.monthrange(date.year, date.month)[1],
    )


def calculate_retirement_date(
    birth_date: datetime.date, retirement_age: int
) -> datetime.date:
    retirement_date = datetime.date(
        year=birth_date.year + retirement_age,
        month=birth_date.month,
        day=birth_date.day,
    )
    return get_last_day_of_month(retirement_date)


def get_next_payment_date(date: datetime.date) -> datetime.date:
    m = (date.month + 1)
    y = date.year
    if m == 13:
        m = 1
        y += 1
    return datetime.date(
        y, m, calendar.monthrange(y, m)[1]
    )


def get_previous_payment_date(date: datetime.date) -> datetime.date:
    m = (date.month - 1)
    y = date.year
    if m == 0:
        m = 12
        y -= 1
    return datetime.date(
        y, m, calendar.monthrange(y, m)[1]
    )


def calculate_payment_date_boundaries(
    birth_date: datetime.date, retirement_age: int, max_age: int
) -> tuple[datetime.date, datetime.date]:
    payment_start_dt = calculate_retirement_date(birth_date, retirement_age)
    payment_end_dt = calculate_retirement_date(birth_date, max_age)
    return payment_start_dt, payment_end_dt


def calculate_stage_flg(
    report_date: datetime.date,
    payment_start_dt: datetime.date,
    payment_end_dt: datetime.date,
) -> int:
    if payment_start_dt <= report_date <= payment_end_dt:
        return 1
    return 0


def get_period_number(
    report_date: datetime.date, payment_start_dt: datetime.date
) -> int:
    if report_date == get_last_day_of_month(report_date):
        payment_date = report_date
    else:
        payment_date = get_previous_payment_date(report_date)
    period_num = (
        payment_date.month
        - payment_start_dt.month
        + 12 * (payment_date.year - payment_start_dt.year)
    )
    if period_num > 0:
        return period_num
    return 0
