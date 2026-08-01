
def spectrogram_signature(x, fs=1.0, window=('tukey_periodic', 0.25), *args, **kwds):
    return array_namespace(x, _skip_if_str_or_tuple(window))

