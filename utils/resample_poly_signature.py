
def resample_poly_signature(x, up, down, axis=0, window=('kaiser', 5.0), *args, **kwds):
    return array_namespace(x, _skip_if_str_or_tuple(window))

