
def numeric_decimal(request):
    """
    Fixture for all numeric formats which should get recognized. The first entry
    represents the value to read while the second represents the expected result.
    """
    return request.param

