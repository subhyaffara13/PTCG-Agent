
def _get_c_intp_name() -> str:
    # Adapted from `np.core._internal._getintp_ctype`
    return {
        "i": "c_int",
        "l": "c_long",
        "q": "c_longlong",
    }.get(np.dtype("n").char, "c_long")

