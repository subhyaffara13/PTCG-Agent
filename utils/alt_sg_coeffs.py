
def alt_sg_coeffs(window_length, polyorder, pos, xp):
    """This is an alternative implementation of the SG coefficients.

    It uses numpy.polyfit and numpy.polyval. The results should be
    equivalent to those of savgol_coeffs(), but this implementation
    is slower.

    window_length should be odd.

    """
    if pos is None:
        pos = window_length // 2
    t = np.arange(window_length)
    unit = (t == pos).astype(int)
    h = np.polyval(np.polyfit(t, unit, polyorder), t)
    return xp.asarray(h)

