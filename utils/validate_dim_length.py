
def validate_dim_length(length: int):
    """
    Validates that an object represents a valid
    dimension length.
    """

    if isinstance(length, (int, torch.SymInt)):
        torch._check(length >= 0)
    else:
        # sometimes called with sympy expression by inductor
        if length < 0:
            raise AssertionError(f"length must be non-negative, got {length}")

