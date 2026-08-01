
def percentile_filter_signature(
    input, percentile, size=None, footprint=None, output=None, *args, **kwds
):
    return array_namespace(input, footprint, _skip_if_dtype(output))

