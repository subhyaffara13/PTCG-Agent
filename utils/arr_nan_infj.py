
def arr_nan_infj(arr_inf):
    with np.errstate(invalid="ignore"):
        return arr_inf * 1j

