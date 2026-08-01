
def mix(request):
    """
    Fixture returning True or False, determining whether to operate
    op(sparse, dense) instead of op(sparse, sparse)
    """
    return request.param

