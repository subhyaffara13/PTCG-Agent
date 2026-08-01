
def _limit_inf(expr, n):
    try:
        return Limit(expr, n, S.Infinity).doit(deep=False)
    except (NotImplementedError, PoleError):
        return None

