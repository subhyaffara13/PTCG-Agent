
def partial_nested_fmt():
    ld = np.dtype("longdouble")
    partial_nested_off = 8 + 8 * (ld.alignment > 8)
    partial_ld_off = partial_ld_offset()
    partial_size = partial_ld_off + ld.itemsize
    partial_end_padding = partial_size % np.dtype("uint64").alignment
    partial_nested_size = partial_nested_off * 2 + partial_size + partial_end_padding
    return "{{'names':['a'],'formats':[{}],'offsets':[{}],'itemsize':{}}}".format(
        partial_dtype_fmt(), partial_nested_off, partial_nested_size
    )

