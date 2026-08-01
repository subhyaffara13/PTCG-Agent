
def interp_methods_ind(request):
    """Fixture that returns a (method name, required kwargs) pair to
    be tested for various Index types.

    This fixture does not include methods - 'time', 'index', 'nearest',
    'values' as a parameterization
    """
    method = request.param
    kwargs = {"order": 1} if method in ("spline", "polynomial") else {}
    return method, kwargs

