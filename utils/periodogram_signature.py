
def periodogram_signature(x, fs=1.0, window='boxcar', *args, **kwds):
    return array_namespace(x, _skip_if_str_or_tuple(window))

