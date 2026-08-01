
def nopython(request):
    """
    Fixture for nopython keyword argument for numba.jit.
    """
    return request.param

