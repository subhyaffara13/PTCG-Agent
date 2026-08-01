
def to_sympy(m, **options):
    """Convert a numpy/scipy.sparse matrix to a SymPy matrix."""
    if isinstance(m, MatrixBase):
        return m
    elif isinstance(m, numpy_ndarray):
        return numpy_to_sympy(m)
    elif isinstance(m, scipy_sparse_matrix):
        return scipy_sparse_to_sympy(m)
    elif isinstance(m, Expr):
        return m
    raise TypeError('Expected sympy/numpy/scipy.sparse matrix, got: %r' % m)

