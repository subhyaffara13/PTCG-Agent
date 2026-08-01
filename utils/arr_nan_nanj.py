
def arr_nan_nanj(arr_nan):
    with np.errstate(invalid="ignore"):
        return arr_nan + arr_nan * 1j

