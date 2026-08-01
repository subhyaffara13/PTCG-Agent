
def resample_signature(x, num, t=None, axis=0, window=None, domain='time'):
    return array_namespace(x, t, _skip_if_str_or_tuple(window))

