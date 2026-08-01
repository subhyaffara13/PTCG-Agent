
def _check_cg(cg_term, expr, length, sign=None):
    """Checks whether a term matches the given expression"""
    # TODO: Check for symmetries
    matches = cg_term.match(expr)
    if matches is None:
        return
    if sign is not None:
        if not isinstance(sign, tuple):
            raise TypeError('sign must be a tuple')
        if not sign[0] == (sign[1]).subs(matches):
            return
    if len(matches) == length:
        return matches

