
def _piecewise_to_heaviside(f, t):
    """
    This function converts a Piecewise expression to an expression written
    with Heaviside. It is not exact, but valid in the context of the Laplace
    transform.
    """
    if not t.is_real:
        r = Dummy('r', real=True)
        return _piecewise_to_heaviside(f.xreplace({t: r}), r).xreplace({r: t})
    x = piecewise_exclusive(f)
    r = []
    for fn, cond in x.args:
        # Here we do not need to do many checks because piecewise_exclusive
        # has a clearly predictable output. However, if any of the conditions
        # is not relative to t, this function just returns the input argument.
        if isinstance(cond, Relational) and t in cond.args:
            if isinstance(cond, (Eq, Ne)):
                # We do not cover this case; these would be single-point
                # exceptions that do not play a role in Laplace practice,
                # except if they contain Dirac impulses, and then we can
                # expect users to not try to use Piecewise for writing it.
                return f
            else:
                r.append(Heaviside(cond.gts - cond.lts)*fn)
        elif isinstance(cond, Or) and len(cond.args) == 2:
            # Or(t<2, t>4), Or(t>4, t<=2), ... in any order with any <= >=
            for c2 in cond.args:
                if c2.lhs == t:
                    r.append(Heaviside(c2.gts - c2.lts)*fn)
                else:
                    return f
        elif isinstance(cond, And) and len(cond.args) == 2:
            # And(t>2, t<4), And(t>4, t<=2), ...  in any order with any <= >=
            c0, c1 = cond.args
            if c0.lhs == t and c1.lhs == t:
                if '>' in c0.rel_op:
                    c0, c1 = c1, c0
                r.append(
                    (Heaviside(c1.gts - c1.lts) -
                     Heaviside(c0.lts - c0.gts))*fn)
            else:
                return f
        else:
            return f
    return Add(*r)

