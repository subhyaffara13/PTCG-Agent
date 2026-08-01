
def arr_complex_nan(arr_complex, arr_nan_nanj):
    with np.errstate(invalid="ignore"):
        return np.vstack([arr_complex, arr_nan_nanj])

