
def _validate_v(v, other, is_other_tuple):
    # This assumes that other is the correct shape, and v should match
    # Both are assumed to be tuples of Tensors
    if len(other) != len(v):
        if is_other_tuple:
            raise RuntimeError(
                f"v is a tuple of invalid length: should be {len(other)} but got {len(v)}."
            )
        else:
            raise RuntimeError("The given v should contain a single Tensor.")

    for idx, (el_v, el_other) in enumerate(zip(v, other)):
        if el_v.size() != el_other.size():
            prepend = ""
            if is_other_tuple:
                prepend = f"Entry {idx} in "
            raise RuntimeError(
                f"{prepend}v has invalid size: should be {el_other.size()} but got {el_v.size()}."
            )

