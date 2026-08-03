from typing import Any

def insert_const_values_with_mask(
    tup: tuple[Any, ...], masks: list[bool], values: tuple[Any, ...]
) -> tuple[Any, ...]:
    """
    masks and values are of same length. For indices where the mask is True, use
    the const_values to fill in.
    """
    out = []
    idx = 0
    for mask_idx, mask in enumerate(masks):
        if mask:
            out.append(values[mask_idx])
        else:
            out.append(tup[idx])
            idx += 1
    return tuple(out)

