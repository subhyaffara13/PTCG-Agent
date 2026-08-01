
def shape_only(shape: TensorShapeType) -> ArrayShaped:
    """Dummy ``numpy.ndarray`` which has a shape only - for generating
    contract expressions.
    """
    return ArrayShaped(shape)

