
def indexer_sli(request):
    """
    Parametrize over __setitem__, loc.__setitem__, iloc.__setitem__
    """
    return request.param

