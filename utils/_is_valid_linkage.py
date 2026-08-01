
def _is_valid_linkage(Z, warning=False, throw=False, name=None,
                      materialize=False, *, xp):
    """Variant of `is_valid_linkage` to be called internally by other scipy functions,
    which by default does not materialize lazy input arrays (Dask, JAX, etc.) when
    warning=True or throw=True.
    """
    name_str = f"{name!r} " if name else ''
    try:
        if Z.dtype != xp.float64:
            raise TypeError(f'Linkage matrix {name_str}must contain doubles.')
        if len(Z.shape) != 2:
            raise ValueError(f'Linkage matrix {name_str}must have shape=2 (i.e. be'
                             ' two-dimensional).')
        if Z.shape[1] != 4:
            raise ValueError(f'Linkage matrix {name_str}must have 4 columns.')
        if Z.shape[0] == 0:
            raise ValueError('Linkage must be computed on at least two '
                             'observations.')
    except (TypeError, ValueError) as e:
        if throw:
            raise
        if warning:
            _warning(str(e))
        return False

    n = Z.shape[0]
    if n < 2:
        return True

    return _lazy_valid_checks(
        (xp.any(Z[:, :2] < 0),
         f'Linkage {name_str}contains negative indices.'),
        (xp.any(Z[:, 2] < 0),
         f'Linkage {name_str}contains negative distances.'),
        (xp.any(Z[:, 3] < 0),
         f'Linkage {name_str}contains negative counts.'),
        (xp.any(Z[:, 3] > n + 1),
         f'Linkage {name_str}contains excessive observations in a cluster'),
        (xp.any(xp.max(Z[:, :2], axis=1) >= xp.arange(n + 1, 2 * n + 1, dtype=Z.dtype)),
         f'Linkage {name_str}uses non-singleton cluster before it is formed.'),
        (xpx.nunique(Z[:, :2]) < n * 2,
         f'Linkage {name_str}uses the same cluster more than once.'),
        throw=throw, warning=warning, materialize=materialize, xp=xp
    )

