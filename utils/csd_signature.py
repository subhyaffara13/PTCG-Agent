
def csd_signature(x, y, fs=1.0, window='hann_periodic', *args, **kwds):
    return array_namespace(x, y, _skip_if_str_or_tuple(window))

