
def _validate_dim(x, dim, offset=0):
    dim = V.graph.sizevars.shape_env.evaluate_expr(sympy.sympify(dim))
    ndim = len(x.get_size())
    if dim < 0:
        dim += ndim + offset
    assert 0 <= dim < ndim + offset
    return dim

