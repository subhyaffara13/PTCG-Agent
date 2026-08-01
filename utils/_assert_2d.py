
def _assert_2d(*arrays):
    for a in arrays:
        if a.ndim != 2:
            raise LinAlgError(f'{a.ndim}-dimensional array given. Array must be '
                              'two-dimensional')

