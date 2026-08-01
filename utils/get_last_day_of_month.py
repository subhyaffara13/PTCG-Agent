
def get_last_day_of_month(year, month):
    # Handle December case
    if month == 12:
        return 31
    # Next month is January, so subtract a day from March 1st
    next_month = datetime(year=year, month=month + 1, day=1)
    last_day_of_month = (next_month - timedelta(days=1)).day
    return last_day_of_month

