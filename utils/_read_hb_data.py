
def _read_hb_data(content, header):
    # XXX: look at a way to reduce memory here (big string creation)
    ptr_string = "".join([content.read(header.pointer_nbytes_full),
                           content.readline()])
    ptr = np.fromstring(ptr_string,
            dtype=int, sep=' ')

    ind_string = "".join([content.read(header.indices_nbytes_full),
                       content.readline()])
    ind = np.fromstring(ind_string,
            dtype=int, sep=' ')

    val_string = "".join([content.read(header.values_nbytes_full),
                          content.readline()])
    val = np.fromstring(val_string,
            dtype=header.values_dtype, sep=' ')

    return csc_array((val, ind-1, ptr-1), shape=(header.nrows, header.ncols))

