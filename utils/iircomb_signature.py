
def iircomb_signature(
    w0, Q, ftype='notch', fs=2.0, *, pass_zero=False, xp=None, device=None
):
    return np_compat if xp is None else xp

