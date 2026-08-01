
def _betaincc(xp, spsx):
    betainc = _get_native_func(xp, spsx, 'betainc')
    if betainc is None:
        return None

    def __betaincc(a, b, x):
        # not perfect; might want to just rely on SciPy
        return betainc(b, a, 1-x)
    return __betaincc

