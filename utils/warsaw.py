
def warsaw(request) -> str:
    """
    tzinfo for Europe/Warsaw using pytz, dateutil, or zoneinfo.
    """
    return request.param

