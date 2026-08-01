
def vectorized_filter_signature(
    input, function, size=None, footprint=None, output=None, *args, **kwds
):
    return array_namespace(input, footprint, _skip_if_dtype(output))

