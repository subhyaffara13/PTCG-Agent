
def split_codes_by_offsets(codes: cpy.CodeArray, offsets: cpy.OffsetArray) -> list[cpy.CodeArray]:
    """Split a code array at locations specified by an offset array into a list of code arrays.
    """
    check_code_array(codes)
    check_offset_array(offsets)

    if len(offsets) > 2:
        return np.split(codes, offsets[1:-1])
    else:
        return [codes]

