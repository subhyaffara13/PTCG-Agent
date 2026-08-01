
def next_workday(dt: datetime) -> datetime:
    """
    returns next workday used for observances
    """
    dt += timedelta(days=1)
    while dt.weekday() > 4:
        # Mon-Fri are 0-4
        dt += timedelta(days=1)
    return dt

