
def _get_nan_val(typecode):
    return {
        "f": np.asarray(np.nan, dtype=np.float32),
        "d": np.asarray(np.nan, dtype=np.float64),
        "g": np.asarray(np.nan, dtype=np.longdouble),
        "F": np.asarray(np.nan + np.nan*1j, dtype=np.complex64),
        "D": np.asarray(np.nan + np.nan*1j, dtype=np.complex128),
        "G": np.asarray(np.nan + np.nan*1j, dtype=np.clongdouble),
    }[typecode]

