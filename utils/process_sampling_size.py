
def process_sampling_size(
    n: int | None, frac: float | None, replace: bool
) -> int | None:
    """
    Process and validate the `n` and `frac` arguments to `NDFrame.sample` and
    `.GroupBy.sample`.

    Returns None if `frac` should be used (variable sampling sizes), otherwise returns
    the constant sampling size.
    """
    # If no frac or n, default to n=1.
    if n is None and frac is None:
        n = 1
    elif n is not None and frac is not None:
        raise ValueError("Please enter a value for `frac` OR `n`, not both")
    elif n is not None:
        if n < 0:
            raise ValueError(
                "A negative number of rows requested. Please provide `n` >= 0."
            )
        if n % 1 != 0:
            raise ValueError("Only integers accepted as `n` values")
    else:
        assert frac is not None  # for mypy
        if frac > 1 and not replace:
            raise ValueError(
                "Replace has to be set to `True` when "
                "upsampling the population `frac` > 1."
            )
        if frac < 0:
            raise ValueError(
                "A negative number of rows requested. Please provide `frac` >= 0."
            )

    return n

