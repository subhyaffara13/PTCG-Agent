
def _parse_minimize(minimize: Union[str, Callable]) -> Tuple[Callable, Union[int, float]]:
    """This works out what local scoring function to use for the dp algorithm
    as well as a `naive_scale` to account for the memory_limit checks.
    """
    if minimize == "flops":
        return _dp_compare_flops, 1
    elif minimize == "size":
        return _dp_compare_size, 1
    elif minimize == "write":
        return _dp_compare_write, 1
    elif callable(minimize):
        # default to naive_scale=inf for this and remaining options
        # as otherwise memory_limit check can cause problems
        return minimize, float("inf")

    # parse out a customized value for the combination factor
    match = minimize_finder.fullmatch(minimize)
    if match is None:
        raise ValueError(f"Couldn't parse `minimize` value: {minimize}.")

    minimize, custom_factor = match.groups()
    factor = float(custom_factor) if custom_factor else DEFAULT_COMBO_FACTOR
    if minimize == "combo":
        return functools.partial(_dp_compare_combo, factor=factor, combine=sum), float("inf")
    elif minimize == "limit":
        return functools.partial(_dp_compare_combo, factor=factor, combine=max), float("inf")
    else:
        raise ValueError(f"Couldn't parse `minimize` value: {minimize}.")

