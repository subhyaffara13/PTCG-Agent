
def observed(request):
    """
    Pass in the observed keyword to groupby for [True, False]
    This indicates whether categoricals should return values for
    values which are not in the grouper [False / None], or only values which
    appear in the grouper [True]. [None] is supported for future compatibility
    if we decide to change the default (and would need to warn if this
    parameter is not passed).
    """
    return request.param

