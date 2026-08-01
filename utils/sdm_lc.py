
def sdm_LC(f, K):
    """Returns the leading coefficient of ``f``. """
    if not f:
        return K.zero
    else:
        return f[0][1]

