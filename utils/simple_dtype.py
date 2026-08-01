
def simple_dtype():
    ld = np.dtype("longdouble")
    return np.dtype(
        {
            "names": ["bool_", "uint_", "float_", "ldbl_"],
            "formats": ["?", "u4", "f4", f"f{ld.itemsize}"],
            "offsets": [0, 4, 8, (16 if ld.alignment > 4 else 12)],
        }
    )

