
from datetime import date


def days_between(start_date: date, end_date: date):
    delta = end_date - start_date
    return delta.days
