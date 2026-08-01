
def matrix_zeros(m, n, **options):
    """"Get a zeros matrix for a given format."""
    format = options.get('format', 'sympy')
    if format == 'sympy':
        return zeros(m, n)
    elif format == 'numpy':
        return _numpy_zeros(m, n, **options)
    elif format == 'scipy.sparse':
        return _scipy_sparse_zeros(m, n, **options)
    raise NotImplementedError('Invaild format: %r' % format)

