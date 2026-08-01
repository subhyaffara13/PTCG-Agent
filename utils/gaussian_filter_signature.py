
def gaussian_filter_signature(input, sigma, order=0, output=None, *args, **kwds):
    return array_namespace(input, _skip_if_dtype(output))

