
def rank_filter_signature(
    input, rank, size=None, footprint=None, output=None, *args, **kwds
):
    return array_namespace(input, footprint, _skip_if_dtype(output))

