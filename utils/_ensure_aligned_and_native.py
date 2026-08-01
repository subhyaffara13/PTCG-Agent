
def _ensure_aligned_and_native(a, overwrite_a):
    """Make sure an input array is aligned and not byteswapped, copy otherwise.
    """
    if not (a.flags['ALIGNED'] and a.dtype.byteorder == '='):
        overwrite_a = True
        a = a.copy()
    return a, overwrite_a

