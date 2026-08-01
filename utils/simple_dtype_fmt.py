
def simple_dtype_fmt():
    ld = np.dtype("longdouble")
    simple_ld_off = 12 + 4 * (ld.alignment > 4)
    return dt_fmt().format(ld.itemsize, simple_ld_off, simple_ld_off + ld.itemsize)

