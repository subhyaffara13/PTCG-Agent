
def _get_month_end_date(today: date) -> date:
    if today.month == 12:
        return date(today.year + 1, 1, 1) - timedelta(days=1)
    return date(today.year, today.month + 1, 1) - timedelta(days=1)

