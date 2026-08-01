
def previous_workday(dt: datetime) -> datetime:
    """
    returns previous workday used for observances
    """
    dt -= timedelta(days=1)
    while dt.weekday() > 4:
        # Mon-Fri are 0-4
        dt -= timedelta(days=1)
    return dt

