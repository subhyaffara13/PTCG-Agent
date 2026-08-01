
def _is_valid_im(R, warning=False, throw=False, name=None, materialize=False, *, xp):
    """Variant of `is_valid_im` to be called internally by other scipy functions,
    which by default does not materialize lazy input arrays (Dask, JAX, etc.) when
    warning=True or throw=True.
    """
    name_str = f"{name!r} " if name else ''
    try:
        if R.dtype != xp.float64:
            raise TypeError(f'Inconsistency matrix {name_str}must contain doubles '
                            '(double).')
        if len(R.shape) != 2:
            raise ValueError(f'Inconsistency matrix {name_str}must have shape=2 (i.e. '
                             'be two-dimensional).')
        if R.shape[1] != 4:
            raise ValueError(f'Inconsistency matrix {name_str}'
                             'must have 4 columns.')
        if R.shape[0] < 1:
            raise ValueError(f'Inconsistency matrix {name_str}'
                             'must have at least one row.')
    except (TypeError, ValueError) as e:
        if throw:
            raise
        if warning:
            _warning(str(e))
        return False

    return _lazy_valid_checks(
        (xp.any(R[:, 0] < 0),
         f'Inconsistency matrix {name_str} contains negative link height means.'),
        (xp.any(R[:, 1] < 0),
         f'Inconsistency matrix {name_str} contains negative link height standard '
         'deviations.'),
        (xp.any(R[:, 2] < 0),
         f'Inconsistency matrix {name_str} contains negative link counts.'),
        throw=throw, warning=warning, materialize=materialize, xp=xp
    )

