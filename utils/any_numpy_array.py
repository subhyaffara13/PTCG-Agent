
def any_numpy_array(request):
    """
    Parametrized fixture for NumPy arrays with different dtypes.

    This excludes string and bytes.
    """
    return request.param.copy()

