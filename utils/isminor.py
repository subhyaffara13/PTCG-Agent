
def isminor(x, ref):
    '''
    This function tests whether x is minor compared to ref. It is used by Powell, e.g., in COBYLA.
    In precise arithmetic, isminor(x, ref) is true if and only if x == 0; in floating point
    arithmetic, isminor(x, ref) is true if x is 0 or its nonzero value can be attributed to
    computer rounding errors according to ref.
    Larger sensitivity means the function is more strict/precise, the value 0.1 being due to Powell.

    For example:
    isminor(1e-20, 1e300) -> True, because in floating point arithmetic 1e-20 cannot be added to
    1e300 without being rounded to 1e300.
    isminor(1e300, 1e-20) -> False, because in floating point arithmetic adding 1e300 to 1e-20
    dominates the latter number.
    isminor(3, 4) -> False, because 3 can be added to 4 without being rounded off
    '''

    sensitivity = 0.1
    refa = abs(ref) + sensitivity * abs(x)
    refb = abs(ref) + 2 * sensitivity * abs(x)
    return np.logical_or(abs(ref) >= refa, refa >= refb)

