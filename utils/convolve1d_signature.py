
def convolve1d_signature(input, weights, axis=-1, output=None, *args, **kwds):
    return array_namespace(input, weights, _skip_if_dtype(output))

