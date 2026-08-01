
def engine_and_read_ext(request):
    """
    Fixture for Excel reader engine and read_ext, only including valid pairs.
    """
    return request.param

