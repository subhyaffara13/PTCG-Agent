
def scipy_sparse_to_sympy(m, **options):
    """Convert a scipy.sparse matrix to a SymPy matrix."""
    return MatrixBase(m.todense())

