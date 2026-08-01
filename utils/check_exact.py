
def check_exact(request):
    """
    Fixture returning `True` or `False`, determining whether to
    compare floating point numbers exactly or not.
    """
    return request.param

