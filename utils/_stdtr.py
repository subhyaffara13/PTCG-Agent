
def _stdtr(xp, spsx):
    betainc = _get_native_func(xp, spsx, 'betainc')
    if betainc is None:
        return None

    def __stdtr(df, t):
        x = df / (t ** 2 + df)
        tail = betainc(df / 2, 0.5, x) / 2
        return xp.where(t < 0, tail, 1 - tail)

    return __stdtr

