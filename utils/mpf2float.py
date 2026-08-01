
def mpf2float(x):
    """
    Convert an mpf to the nearest floating point number. Just using
    float directly doesn't work because of results like this:

    with mp.workdps(50):
        float(mpf("0.99999999999999999")) = 0.9999999999999999

    """
    return float(mpmath.nstr(x, 17, min_fixed=0, max_fixed=0))

