
def morphological_gradient_signature(
    input, size=None, footprint=None, structure=None, output=None, *args, **kwds
):
    return array_namespace(input, footprint, structure, _skip_if_dtype(output))

