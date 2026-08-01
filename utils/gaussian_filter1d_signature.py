
def gaussian_filter1d_signature(
    input, sigma, axis=-1, order=0, output=None, *args, **kwds
):
    return array_namespace(input, _skip_if_dtype(output))

