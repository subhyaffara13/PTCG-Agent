
def outer_offsets_from_list_of_offsets(list_of_offsets: list[cpy.OffsetArray]) -> cpy.OffsetArray:
    """Determine outer offsets from a list of offsets.
    """
    if not list_of_offsets:
        raise ValueError("Empty list passed to outer_offsets_from_list_of_offsets")

    return np.cumsum([0] + [len(offsets)-1 for offsets in list_of_offsets], dtype=offset_dtype)

