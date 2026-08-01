
def _piecewise_simplify_equal_to_next_segment(args):
    """
    See if expressions valid for an Equal expression happens to evaluate
    to the same function as in the next piecewise segment, see:
    https://github.com/sympy/sympy/issues/8458
    """
    prevexpr = None
    for i, (expr, cond) in reversed(list(enumerate(args))):
        if prevexpr is not None:
            if isinstance(cond, And):
                eqs, other = sift(cond.args,
                                  lambda i: isinstance(i, Eq), binary=True)
            elif isinstance(cond, Eq):
                eqs, other = [cond], []
            else:
                eqs = other = []
            _prevexpr = prevexpr
            _expr = expr
            if eqs and not other:
                eqs = list(ordered(eqs))
                for e in eqs:
                    # allow 2 args to collapse into 1 for any e
                    # otherwise limit simplification to only simple-arg
                    # Eq instances
                    if len(args) == 2 or _blessed(e):
                        _prevexpr = _prevexpr.subs(*e.args)
                        _expr = _expr.subs(*e.args)
            # Did it evaluate to the same?
            if _prevexpr == _expr:
                # Set the expression for the Not equal section to the same
                # as the next. These will be merged when creating the new
                # Piecewise
                args[i] = args[i].func(args[i + 1][0], cond)
            else:
                # Update the expression that we compare against
                prevexpr = expr
        else:
            prevexpr = expr
    return args

