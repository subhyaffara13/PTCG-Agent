
def uniform_filter_signature(input, size=3, output=None, *args, **kwds):
    return array_namespace(input, _skip_if_dtype(output))

