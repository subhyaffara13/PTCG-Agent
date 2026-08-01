
def swap_byteorder(arr):
    """Returns the same array with swapped byteorder"""
    dtype = arr.dtype.newbyteorder('S')
    return arr.astype(dtype)

