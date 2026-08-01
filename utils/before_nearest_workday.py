
def before_nearest_workday(dt: datetime) -> datetime:
    """
    returns previous workday before nearest workday
    """
    return previous_workday(nearest_workday(dt))

