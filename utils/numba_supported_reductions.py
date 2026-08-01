
def numba_supported_reductions(request):
    """reductions supported with engine='numba'"""
    return request.param

