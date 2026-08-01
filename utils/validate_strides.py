
def validate_strides(strides: StrideType):
    """
    Verifies the object specifies valid strides.
    """

    if not isinstance(strides, Sequence):
        raise AssertionError(f"strides must be a Sequence, got {type(strides)}")
    for stride in strides:
        if stride < 0:
            raise AssertionError(f"stride must be non-negative, got {stride}")

