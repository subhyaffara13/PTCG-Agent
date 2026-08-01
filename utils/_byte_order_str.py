
def _byte_order_str(dtype):
    """ Normalize byteorder to '<' or '>' """
    # hack to obtain the native and swapped byte order characters
    swapped = np.dtype(int).newbyteorder('S')
    native = swapped.newbyteorder('S')

    byteorder = dtype.byteorder
    if byteorder == '=':
        return native.byteorder
    if byteorder == 'S':
        # TODO: this path can never be reached
        return swapped.byteorder
    elif byteorder == '|':
        return ''
    else:
        return byteorder

