
def _vsolve(e, s, **flags):
    """return list of scalar values for the solution of e for symbol s"""
    return [i[s] for i in _solve(e, s, **flags)]

