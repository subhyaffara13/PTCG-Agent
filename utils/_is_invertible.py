
def _is_invertible(a, b, sign):
    """
    Checks whether a given pair of MIMO
    systems passed is invertible or not.
    """
    _mat = eye(a.num_outputs) - sign*(a.doit()._expr_mat)*(b.doit()._expr_mat)
    _det = _mat.det()

    return _det != 0

