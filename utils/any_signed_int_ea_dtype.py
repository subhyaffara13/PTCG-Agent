
def any_signed_int_ea_dtype(request):
    """
    Parameterized fixture for any signed nullable integer dtype.

    * 'Int8'
    * 'Int16'
    * 'Int32'
    * 'Int64'
    """
    return request.param

