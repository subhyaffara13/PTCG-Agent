
def binary_dilation_signature(
    input, structure=None, iterations=1, mask=None, output=None, *args, **kwds
):
    return array_namespace(input, structure, _skip_if_dtype(output), mask)

