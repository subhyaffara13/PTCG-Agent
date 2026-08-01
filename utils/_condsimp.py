
def _condsimp(cond, first=True):
    """
    Do naive simplifications on ``cond``.

    Explanation
    ===========

    Note that this routine is completely ad-hoc, simplification rules being
    added as need arises rather than following any logical pattern.

    Examples
    ========

    >>> from sympy.integrals.meijerint import _condsimp as simp
    >>> from sympy import Or, Eq
    >>> from sympy.abc import x, y
    >>> simp(Or(x < y, Eq(x, y)))
    x <= y
    """
    if first:
        cond = cond.replace(lambda _: _.is_Relational, _canonical_coeff)
        first = False
    if not isinstance(cond, BooleanFunction):
        return cond
    p, q, r = symbols('p q r', cls=Wild)
    # transforms tests use 0, 4, 5 and 11-14
    # meijer tests use 0, 2, 11, 14
    # joint_rv uses 6, 7
    rules = [
        (Or(p < q, Eq(p, q)), p <= q),  # 0
        # The next two obviously are instances of a general pattern, but it is
        # easier to spell out the few cases we care about.
        (And(Abs(arg(p)) <= pi, Abs(arg(p) - 2*pi) <= pi),
         Eq(arg(p) - pi, 0)),  # 1
        (And(Abs(2*arg(p) + pi) <= pi, Abs(2*arg(p) - pi) <= pi),
         Eq(arg(p), 0)), # 2
        (And(Abs(2*arg(p) + pi) < pi, Abs(2*arg(p) - pi) <= pi),
         S.false),  # 3
        (And(Abs(arg(p) - pi/2) <= pi/2, Abs(arg(p) + pi/2) <= pi/2),
         Eq(arg(p), 0)),  # 4
        (And(Abs(arg(p) - pi/2) <= pi/2, Abs(arg(p) + pi/2) < pi/2),
         S.false),  # 5
        (And(Abs(arg(p**2/2 + 1)) < pi, Ne(Abs(arg(p**2/2 + 1)), pi)),
         S.true),  # 6
        (Or(Abs(arg(p**2/2 + 1)) < pi, Ne(1/(p**2/2 + 1), 0)),
         S.true),  # 7
        (And(Abs(unbranched_argument(p)) <= pi,
           Abs(unbranched_argument(exp_polar(-2*pi*S.ImaginaryUnit)*p)) <= pi),
         Eq(unbranched_argument(exp_polar(-S.ImaginaryUnit*pi)*p), 0)),  # 8
        (And(Abs(unbranched_argument(p)) <= pi/2,
           Abs(unbranched_argument(exp_polar(-pi*S.ImaginaryUnit)*p)) <= pi/2),
         Eq(unbranched_argument(exp_polar(-S.ImaginaryUnit*pi/2)*p), 0)),  # 9
        (Or(p <= q, And(p < q, r)), p <= q),  # 10
        (Ne(p**2, 1) & (p**2 > 1), p**2 > 1),  # 11
        (Ne(1/p, 1) & (cos(Abs(arg(p)))*Abs(p) > 1), Abs(p) > 1),  # 12
        (Ne(p, 2) & (cos(Abs(arg(p)))*Abs(p) > 2), Abs(p) > 2),  # 13
        ((Abs(arg(p)) < pi/2) & (cos(Abs(arg(p)))*sqrt(Abs(p**2)) > 1), p**2 > 1),  # 14
    ]
    cond = cond.func(*[_condsimp(_, first) for _ in cond.args])
    change = True
    while change:
        change = False
        for irule, (fro, to) in enumerate(rules):
            if fro.func != cond.func:
                continue
            for n, arg1 in enumerate(cond.args):
                if r in fro.args[0].free_symbols:
                    m = arg1.match(fro.args[1])
                    num = 1
                else:
                    num = 0
                    m = arg1.match(fro.args[0])
                if not m:
                    continue
                otherargs = [x.subs(m) for x in fro.args[:num] + fro.args[num + 1:]]
                otherlist = [n]
                for arg2 in otherargs:
                    for k, arg3 in enumerate(cond.args):
                        if k in otherlist:
                            continue
                        if arg2 == arg3:
                            otherlist += [k]
                            break
                        if isinstance(arg3, And) and arg2.args[1] == r and \
                                isinstance(arg2, And) and arg2.args[0] in arg3.args:
                            otherlist += [k]
                            break
                        if isinstance(arg3, And) and arg2.args[0] == r and \
                                isinstance(arg2, And) and arg2.args[1] in arg3.args:
                            otherlist += [k]
                            break
                if len(otherlist) != len(otherargs) + 1:
                    continue
                newargs = [arg_ for (k, arg_) in enumerate(cond.args)
                           if k not in otherlist] + [to.subs(m)]
                if SYMPY_DEBUG:
                    if irule not in (0, 2, 4, 5, 6, 7, 11, 12, 13, 14):
                        print('used new rule:', irule)
                cond = cond.func(*newargs)
                change = True
                break

    # final tweak
    def rel_touchup(rel):
        if rel.rel_op != '==' or rel.rhs != 0:
            return rel

        # handle Eq(*, 0)
        LHS = rel.lhs
        m = LHS.match(arg(p)**q)
        if not m:
            m = LHS.match(unbranched_argument(polar_lift(p)**q))
        if not m:
            if isinstance(LHS, periodic_argument) and not LHS.args[0].is_polar \
                    and LHS.args[1] is S.Infinity:
                return (LHS.args[0] > 0)
            return rel
        return (m[p] > 0)
    cond = cond.replace(lambda _: _.is_Relational, rel_touchup)
    if SYMPY_DEBUG:
        print('_condsimp: ', cond)
    return cond

