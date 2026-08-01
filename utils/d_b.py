
def dB(x):
    # Return magnitude in decibels, avoiding divide-by-zero warnings
    # (and deal with some "not less-ordered" errors when -inf shows up)
    xp = array_namespace(x)
    tiny = xp.asarray(np.finfo(np.float64).tiny)
    return 20 * xp.log10(xp.maximum(xp.abs(x), tiny))

