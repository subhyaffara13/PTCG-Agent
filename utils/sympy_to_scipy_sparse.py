
def sympy_to_scipy_sparse(m, **options):
    """Convert a SymPy Matrix/complex number to a numpy matrix or scalar."""
    if not np or not sparse:
        raise ImportError
    dtype = options.get('dtype', 'complex')
    if isinstance(m, MatrixBase):
        return sparse.csr_matrix(np.array(m.tolist(), dtype=dtype))
    elif isinstance(m, Expr):
        if m.is_Number or m.is_NumberSymbol or m == I:
            return complex(m)
    raise TypeError('Expected MatrixBase or complex scalar, got: %r' % m)

