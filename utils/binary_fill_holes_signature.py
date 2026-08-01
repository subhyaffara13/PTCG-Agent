
def binary_fill_holes_signature(
    input, structure=None, output=None, origin=0, *args, **kwargs
):
    return array_namespace(input, structure, _skip_if_dtype(output))

