
def _domain_check(f, symbol, p):
    # helper for domain check
    if f.is_Atom and f.is_finite:
        return True
    elif f.subs(symbol, p).is_infinite:
        return False
    elif isinstance(f, Piecewise):
        # Check the cases of the Piecewise in turn. There might be invalid
        # expressions in later cases that don't apply e.g.
        #    solveset(Piecewise((0, Eq(x, 0)), (1/x, True)), x)
        for expr, cond in f.args:
            condsubs = cond.subs(symbol, p)
            if condsubs is S.false:
                continue
            elif condsubs is S.true:
                return _domain_check(expr, symbol, p)
            else:
                # We don't know which case of the Piecewise holds. On this
                # basis we cannot decide whether any solution is in or out of
                # the domain. Ideally this function would allow returning a
                # symbolic condition for the validity of the solution that
                # could be handled in the calling code. In the mean time we'll
                # give this particular solution the benefit of the doubt and
                # let it pass.
                return True
    else:
        # TODO : We should not blindly recurse through all args of arbitrary expressions like this
        return all(_domain_check(g, symbol, p)
                   for g in f.args)

