
def _giant_steps(target):
    """Return a list of precision steps for the Newton's method"""
    # We use ceil here because giant_steps cannot handle flint.fmpq
    res = giant_steps(2, math.ceil(target))
    if res[0] != 2:
        res = [2] + res
    return res

