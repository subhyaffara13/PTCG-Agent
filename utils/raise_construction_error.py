
def raise_construction_error(
    tot_items: int,
    block_shape: Shape,
    axes: list[Index],
    e: ValueError | None = None,
) -> NoReturn:
    """raise a helpful message about our construction"""
    passed = tuple(map(int, [tot_items, *block_shape]))
    # Correcting the user facing error message during dataframe construction
    if len(passed) <= 2:
        passed = passed[::-1]

    implied = tuple(len(ax) for ax in axes)
    # Correcting the user facing error message during dataframe construction
    if len(implied) <= 2:
        implied = implied[::-1]

    # We return the exception object instead of raising it so that we
    #  can raise it in the caller; mypy plays better with that
    if passed == implied and e is not None:
        raise e
    if block_shape[0] == 0:
        raise ValueError("Empty data passed with indices specified.")
    raise ValueError(f"Shape of passed values is {passed}, indices imply {implied}")

