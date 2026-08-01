
def affine_transform_signature(
    input, matrix, offset=0.0, output_shape=None, output=None, *args, **kwds
):
    return array_namespace(input, matrix, _skip_if_dtype(output))

