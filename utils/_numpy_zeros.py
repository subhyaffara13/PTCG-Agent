
def _numpy_zeros(m, n, **options):
    """numpy version of zeros."""
    dtype = options.get('dtype', 'float64')
    if not np:
        raise ImportError
    return np.zeros((m, n), dtype=dtype)

