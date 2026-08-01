
def partial_dtype_fmt():
    ld = np.dtype("longdouble")
    partial_ld_off = partial_ld_offset()
    partial_size = partial_ld_off + ld.itemsize
    partial_end_padding = partial_size % np.dtype("uint64").alignment
    return dt_fmt().format(
        ld.itemsize, partial_ld_off, partial_size + partial_end_padding
    )

