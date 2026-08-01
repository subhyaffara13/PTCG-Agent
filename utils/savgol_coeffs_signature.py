
def savgol_coeffs_signature(
    window_length, polyorder, deriv=0, delta=1.0, pos=None, use='conv',
    *, xp=None, device=None
):
    return np if xp is None else xp

