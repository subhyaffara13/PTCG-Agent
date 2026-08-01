
def string_dtype(request):
    """
    Parametrized fixture for string dtypes.

    * str
    * 'str'
    * 'U'
    """
    return request.param

