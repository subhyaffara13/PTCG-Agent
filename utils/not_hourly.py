
def not_hourly(request):
    """
    Several timedelta-like and DateOffset instances that are _not_
    compatible with Hourly frequencies.
    """
    return request.param

