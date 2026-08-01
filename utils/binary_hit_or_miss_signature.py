
def binary_hit_or_miss_signature(
    input, structure1=None, structure2=None, output=None, *args, **kwds
):
    return array_namespace(input, structure1, structure2, _skip_if_dtype(output))

