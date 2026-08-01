
def _siegelslopes(y, x=None, method="hierarchical"):
    if method not in ['hierarchical', 'separate']:
        raise ValueError("method can only be 'hierarchical' or 'separate'")
    y = np.asarray(y).ravel()
    if x is None:
        x = np.arange(len(y), dtype=float)
    else:
        x = np.asarray(x, dtype=float).ravel()
        if len(x) != len(y):
            raise ValueError("Array shapes are incompatible for broadcasting.")
    if len(x) < 2:
        raise ValueError("`x` and `y` must have length at least 2.")

    dtype = np.result_type(x, y, np.float32)  # use at least float32
    y, x = y.astype(dtype), x.astype(dtype)
    medslope, medinter = siegelslopes_pythran(y, x, method)
    medslope, medinter = np.asarray(medslope)[()], np.asarray(medinter)[()]
    return SiegelslopesResult(slope=medslope, intercept=medinter)

