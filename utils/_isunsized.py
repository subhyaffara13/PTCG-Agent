
def _isunsized(dtype):
    # PyDataType_ISUNSIZED
    return dtype.itemsize == 0

