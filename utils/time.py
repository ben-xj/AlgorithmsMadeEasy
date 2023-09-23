
from datetime import date


def days_between(start_date: date, end_date: date):
    delta = end_date - start_date
    return delta.days


def date_to_str(date_obj: date, format_str="%Y-%m-%d"):
    """
    Convert a date object to a string in the specified format.

    Args:
        date_obj (datetime.date): The date object to be converted.
        format_str (str): The format string to use for the conversion. Default is "%Y-%m-%d".

    Returns:
        str: The date as a string in the specified format.
    """
    return date_obj.strftime(format_str)
