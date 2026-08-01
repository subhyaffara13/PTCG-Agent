
def _stdtrit(xp, spsx):
    # Need either native stdtr or native betainc
    stdtr = _get_native_func(xp, spsx, 'stdtr') or _stdtr(xp, spsx)
    # If betainc is not defined, the root-finding would be done with `xp`
    # despite `stdtr` being evaluated with SciPy/NumPy `stdtr`. Save the
    # conversions: in this case, just evaluate `stdtrit` with SciPy/NumPy.
    if stdtr is None:
        return None

    from scipy.optimize.elementwise import bracket_root, find_root

    def __stdtrit(df, p):
        def fun(t, df, p):  return stdtr(df, t) - p
        res_bracket = bracket_root(fun, xp.zeros_like(p), args=(df, p))
        res_root = find_root(fun, res_bracket.bracket, args=(df, p))
        return res_root.x

    return __stdtrit

