
def offsets_from_codes(codes: cpy.CodeArray) -> cpy.OffsetArray:
    """Determine offsets from codes using locations of MOVETO codes.
    """
    check_code_array(codes)

    return np.append(np.nonzero(codes == MOVETO)[0], len(codes)).astype(offset_dtype)

