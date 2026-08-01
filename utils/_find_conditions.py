
def _find_conditions(func, x, x0, order, evalf=False, use_limit=True):
    y0 = []
    for _ in range(order):
        val = func.subs(x, x0)
        if evalf:
            val = val.evalf()
        if use_limit and isinstance(val, NaN):
            val = limit(func, x, x0)
        if val.is_finite is False or isinstance(val, NaN):
            return None
        y0.append(val)
        func = func.diff(x)
    return y0

