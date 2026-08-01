
def _check_work_float(value, dtype, int_dtype):
    """
    Convert LAPACK-returned work array size float to integer,
    carefully for single-precision types.
    """

    if dtype == np.float32 or dtype == np.complex64:
        # Single-precision routine -- take next fp value to work
        # around possible truncation in LAPACK code
        value = np.nextafter(value, np.inf, dtype=np.float32)

    value = int(value)
    if int_dtype.itemsize == 4:
        if value < 0 or value > _int32_max:
            raise ValueError("Too large work array required -- computation "
                             "cannot be performed with standard 32-bit"
                             " LAPACK.")
    elif int_dtype.itemsize == 8:
        if value < 0 or value > _int64_max:
            raise ValueError("Too large work array required -- computation"
                             " cannot be performed with standard 64-bit"
                             " LAPACK.")
    return value

