
def _validate_sizes(n, m):
    if n < 1 or not isinstance(n, numbers.Integral):
        raise ValueError('Invalid number of CZT data '
                         f'points ({n}) specified. '
                         'n must be positive and integer type.')

    if m is None:
        m = n
    elif m < 1 or not isinstance(m, numbers.Integral):
        raise ValueError('Invalid number of CZT output '
                         f'points ({m}) specified. '
                         'm must be positive and integer type.')

    return m

