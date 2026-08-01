
def check_index_type(request):
    """
    Fixture returning `True` or `False`, determining whether to check
    if the `Index` types are identical or not.
    """
    return request.param

