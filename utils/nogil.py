
def nogil(request):
    """
    Fixture for nogil keyword argument for numba.jit.
    """
    return request.param

