
def pair_different_warnings(request):
    """
    Return pair or different warnings.

    Useful for testing how several different warnings are handled
    in tm.assert_produces_warning.
    """
    return request.param

