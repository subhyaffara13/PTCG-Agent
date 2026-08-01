
def check_categorical(request):
    """
    Fixture returning `True` or `False`, determining whether to
    compare internal `Categorical` exactly or not.
    """
    return request.param

