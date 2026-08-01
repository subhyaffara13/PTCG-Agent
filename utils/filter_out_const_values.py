
def filter_out_const_values(tup: tuple[Any, ...], masks: list[bool]) -> tuple[Any, ...]:
    """
    masks is a list of bools, where True means the corresponding element in tup
    is a const value. Filter out the const values.
    """
    out = []
    for mask_idx, mask in enumerate(masks):
        if not mask:
            out.append(tup[mask_idx])
    return tuple(out)

