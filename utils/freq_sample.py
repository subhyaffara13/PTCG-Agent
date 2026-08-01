
def freq_sample(request):
    """
    Valid values for 'freq' parameter used to create date_range and
    timedelta_range..
    """
    return request.param

