
def arr_complex_nan_infj(arr_complex, arr_nan_infj):
    with np.errstate(invalid="ignore"):
        return np.vstack([arr_complex, arr_nan_infj])

