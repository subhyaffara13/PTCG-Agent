
def get_tolerances(
    *inputs: torch.Tensor | torch.dtype,
    rtol: float | None,
    atol: float | None,
    id: tuple[Any, ...] = (),
) -> tuple[float, float]:
    """Gets absolute and relative to be used for numeric comparisons.

    If both ``rtol`` and ``atol`` are specified, this is a no-op. If both are not specified, the return value of
    :func:`default_tolerances` is used.

    Raises:
        ErrorMeta: With :class:`ValueError`, if only ``rtol`` or ``atol`` is specified.

    Returns:
        (Tuple[float, float]): Valid absolute and relative tolerances.
    """
    if (rtol is None) ^ (atol is None):
        # We require both tolerance to be omitted or specified, because specifying only one might lead to surprising
        # results. Imagine setting atol=0.0 and the tensors still match because rtol>0.0.
        raise ErrorMeta(
            ValueError,
            f"Both 'rtol' and 'atol' must be either specified or omitted, "
            f"but got no {'rtol' if rtol is None else 'atol'}.",
            id=id,
        )
    elif rtol is not None and atol is not None:
        return rtol, atol
    else:
        return default_tolerances(*inputs)

