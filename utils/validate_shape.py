
def validate_shape(shape: ShapeType):
    """
    Validates that a sequence represents a valid shape.
    """

    if not isinstance(shape, Sequence):
        raise AssertionError(f"shape must be a Sequence, got {type(shape)}")
    for l in shape:
        validate_dim_length(l)

