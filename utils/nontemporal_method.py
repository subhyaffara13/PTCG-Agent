
def nontemporal_method(request):
    """Fixture that returns an (method name, required kwargs) pair.

    This fixture does not include method 'time' as a parameterization; that
    method requires a Series with a DatetimeIndex, and is generally tested
    separately from these non-temporal methods.
    """
    method = request.param
    kwargs = {"order": 1} if method in ("spline", "polynomial") else {}
    return method, kwargs

