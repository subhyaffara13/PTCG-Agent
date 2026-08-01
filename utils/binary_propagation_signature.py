
def binary_propagation_signature(
    input, structure=None, mask=None, output=None, *args, **kwds
):
    return array_namespace(input, structure, mask, _skip_if_dtype(output))

