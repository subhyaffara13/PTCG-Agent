
def _assert_stacked_square(*arrays):
    for a in arrays:
        try:
            m, n = a.shape[-2:]
        except ValueError:
            raise LinAlgError(f'{a.ndim}-dimensional array given. Array must be '
                              'at least two-dimensional')
        if m != n:
            raise LinAlgError('Last 2 dimensions of the array must be square')

