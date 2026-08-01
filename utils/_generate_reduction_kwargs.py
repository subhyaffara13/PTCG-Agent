
def _generate_reduction_kwargs(ndim, supports_multiple_dims=True):
    """Generates a subset of all valid dim and keepdim kwargs given ndim that
    is appropriate for testing reduction operators.
    """

    # Test default dim and keepdim
    yield {}

    # Test reducing inner and outer most dimensions
    yield {"dim": 0, "keepdim": True}
    yield {"dim": -1, "keepdim": False}

    # Test reducing middle dimension
    if ndim > 2:
        yield {"dim": ndim // 2, "keepdim": True}

    if supports_multiple_dims:
        # Test reducing all dimensions
        yield {"dim": tuple(range(ndim)), "keepdim": False}

        # Test reducing both first and last dimensions
        if ndim > 1:
            yield {"dim": (0, -1), "keepdim": True}

        # Test reducing every other dimension starting with the second
        if ndim > 3:
            yield {"dim": tuple(range(1, ndim, 2)), "keepdim": False}

