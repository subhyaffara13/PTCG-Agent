
def _validate_pdist_input(X, m, n, metric_info, **kwargs):
    # get supported types
    types = metric_info.types
    # choose best type
    typ = types[types.index(X.dtype)] if X.dtype in types else types[0]
    # validate data
    X = _convert_to_type(X, out_type=typ)

    # validate kwargs
    _validate_kwargs = metric_info.validator
    if _validate_kwargs:
        kwargs = _validate_kwargs(X, m, n, **kwargs)
    return X, typ, kwargs

