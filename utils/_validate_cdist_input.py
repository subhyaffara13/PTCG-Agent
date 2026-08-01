
def _validate_cdist_input(XA, XB, mA, mB, n, metric_info, **kwargs):
    # get supported types
    types = metric_info.types
    # choose best type
    typ = types[types.index(XA.dtype)] if XA.dtype in types else types[0]
    # validate data
    XA = _convert_to_type(XA, out_type=typ)
    XB = _convert_to_type(XB, out_type=typ)

    # validate kwargs
    _validate_kwargs = metric_info.validator
    if _validate_kwargs:
        kwargs = _validate_kwargs((XA, XB), mA + mB, n, **kwargs)
    return XA, XB, typ, kwargs

