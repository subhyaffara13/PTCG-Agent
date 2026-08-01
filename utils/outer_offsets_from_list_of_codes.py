
def outer_offsets_from_list_of_codes(list_of_codes: list[cpy.CodeArray]) -> cpy.OffsetArray:
    """Determine outer offsets from codes using locations of MOVETO codes.
    """
    if not list_of_codes:
        raise ValueError("Empty list passed to outer_offsets_from_list_of_codes")

    return np.cumsum([0] + [np.count_nonzero(codes == MOVETO) for codes in list_of_codes],
                     dtype=offset_dtype)

