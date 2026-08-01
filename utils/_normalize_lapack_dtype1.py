
def _normalize_lapack_dtype1(a, overwrite_a):
    if a.dtype.char not in 'fdFD':
        dtype_char = _lapack_cast_dict[a.dtype.char]
        if not dtype_char:  # No casting possible
            raise TypeError(f'The dtype {a.dtype} cannot be cast '
                            'to float(32, 64) or complex(64, 128).')

        a = a.astype(dtype_char[0])  # makes a copy, free to scratch
        overwrite_a = True
    return a, overwrite_a

