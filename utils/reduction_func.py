
def reduction_func(request):
    """
    yields the string names of all groupby reduction functions, one at a time.
    """
    return request.param

