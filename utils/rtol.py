
def rtol(request):
    """
    Fixture returning 0.5e-3 or 0.5e-5. Those values are used as relative tolerance.
    """
    return request.param

