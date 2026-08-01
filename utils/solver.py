
def solver(request):
    """
    Fixture for all solvers in scipy.sparse.linalg._isolve
    """
    return request.param

