import sys

def _make_options_dict(precision=None, threshold=None, edgeitems=None,
                       linewidth=None, suppress=None, nanstr=None, infstr=None,
                       sign=None, formatter=None, floatmode=None, legacy=None,
                       override_repr=None):
    """
    Make a dictionary out of the non-None arguments, plus conversion of
    *legacy* and sanity checks.
    """

    options = {k: v for k, v in list(locals().items()) if v is not None}

    if suppress is not None:
        options['suppress'] = bool(suppress)

    modes = ['fixed', 'unique', 'maxprec', 'maxprec_equal']
    if floatmode not in modes + [None]:
        raise ValueError("floatmode option must be one of " +
                         ", ".join(f'"{m}"' for m in modes))

    if sign not in [None, '-', '+', ' ']:
        raise ValueError("sign option must be one of ' ', '+', or '-'")

    if legacy is False:
        options['legacy'] = sys.maxsize
    elif legacy == False:
        warnings.warn(
            f"Passing `legacy={legacy!r}` is deprecated.",
            FutureWarning, stacklevel=3
        )
        options['legacy'] = sys.maxsize
    elif legacy == '1.13':
        options['legacy'] = 113
    elif legacy == '1.21':
        options['legacy'] = 121
    elif legacy == '1.25':
        options['legacy'] = 125
    elif legacy == '2.1':
        options['legacy'] = 201
    elif legacy == '2.2':
        options['legacy'] = 202
    elif legacy is None:
        pass  # OK, do nothing.
    else:
        warnings.warn(
            "legacy printing option can currently only be '1.13', '1.21', "
            "'1.25', '2.1', '2.2' or `False`", stacklevel=3)

    if threshold is not None:
        # forbid the bad threshold arg suggested by stack overflow, gh-12351
        if not isinstance(threshold, numbers.Number):
            raise TypeError("threshold must be numeric")
        if np.isnan(threshold):
            raise ValueError("threshold must be non-NAN, try "
                             "sys.maxsize for untruncated representation")

    if precision is not None:
        # forbid the bad precision arg as suggested by issue #18254
        try:
            options['precision'] = operator.index(precision)
        except TypeError as e:
            raise TypeError('precision must be an integer') from e

    return options

