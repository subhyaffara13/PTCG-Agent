
def geometric_transform_signature(
    input, mapping, output_shape=None, output=None, *args, **kwds
):
    return array_namespace(input, _skip_if_dtype(output))

