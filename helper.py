import datetime


def get_current_date():
    """Function that returns 2 date strings:
    1 - yyyy-month: "2022-august"
    2 - dd-mm-yyyy: "07-08-2022"
    """
    now = datetime.date.today()
    year_month_str = now.strftime("%Y-%B")
    date_str = now.strftime("%d-%m-%Y")

    return year_month_str, date_str
