
def istft_signature(Zxx, fs=1.0, window='hann_periodic', *args, **kwds):
    return array_namespace(Zxx, _skip_if_str_or_tuple(window))

