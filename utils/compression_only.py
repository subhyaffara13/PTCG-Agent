
def compression_only(request):
    """
    Fixture for trying common compression types in compression tests excluding
    uncompressed case.
    """
    return request.param

