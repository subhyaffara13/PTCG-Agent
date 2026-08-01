
def unique_nulls_fixture(request):
    """
    Fixture for each null type in pandas, each null type exactly once.
    """
    return request.param

