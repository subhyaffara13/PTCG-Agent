
def _read_data(f, dtype):
    '''Read a variable with a specified data type'''
    if dtype == 1:
        if _read_int32(f) != 1:
            raise Exception("Error occurred while reading byte variable")
        return _read_byte(f)
    elif dtype == 2:
        return _read_int16(f)
    elif dtype == 3:
        return _read_int32(f)
    elif dtype == 4:
        return _read_float32(f)
    elif dtype == 5:
        return _read_float64(f)
    elif dtype == 6:
        real = _read_float32(f)
        imag = _read_float32(f)
        return np.complex64(real + imag * 1j)
    elif dtype == 7:
        return _read_string_data(f)
    elif dtype == 8:
        raise Exception("Should not be here - please report this")
    elif dtype == 9:
        real = _read_float64(f)
        imag = _read_float64(f)
        return np.complex128(real + imag * 1j)
    elif dtype == 10:
        return Pointer(_read_int32(f))
    elif dtype == 11:
        return ObjectPointer(_read_int32(f))
    elif dtype == 12:
        return _read_uint16(f)
    elif dtype == 13:
        return _read_uint32(f)
    elif dtype == 14:
        return _read_int64(f)
    elif dtype == 15:
        return _read_uint64(f)
    else:
        raise Exception(f"Unknown IDL type: {dtype} - please report this")

