
def _rel_as_nonpos(constr, syms):
    """return `(np, d, aux)` where `np` is a list of nonpositive
    expressions that represent the given constraints (possibly
    rewritten in terms of auxilliary variables) expressible with
    nonnegative symbols, and `d` is a dictionary mapping a given
    symbols to an expression with an auxilliary variable. In some
    cases a symbol will be used as part of the change of variables,
    e.g. x: x - z1 instead of x: z1 - z2.

    If any constraint is False/empty, return None. All variables in
    ``constr`` are assumed to be unbounded unless explicitly indicated
    otherwise with a univariate constraint, e.g. ``x >= 0`` will
    restrict ``x`` to nonnegative values.

    The ``syms`` must be included so all symbols can be given an
    unbounded assumption if they are not otherwise bound with
    univariate conditions like ``x <= 3``.

    Examples
    ========

    >>> from sympy.solvers.simplex import _rel_as_nonpos
    >>> from sympy.abc import x, y
    >>> _rel_as_nonpos([x >= y, x >= 0, y >= 0], (x, y))
    ([-x + y], {}, [])
    >>> _rel_as_nonpos([x >= 3, x <= 5], [x])
    ([_z1 - 2], {x: _z1 + 3}, [_z1])
    >>> _rel_as_nonpos([x <= 5], [x])
    ([], {x: 5 - _z1}, [_z1])
    >>> _rel_as_nonpos([x >= 1], [x])
    ([], {x: _z1 + 1}, [_z1])
    """
    r = {}  # replacements to handle change of variables
    np = []  # nonpositive expressions
    aux = []  # auxilliary symbols added
    ui = numbered_symbols("z", start=1, cls=Dummy)  # auxilliary symbols
    univariate = {}  # {x: interval} for univariate constraints
    unbound = []  # symbols designated as unbound
    syms = set(syms)  # the expected syms of the system

    # separate out univariates
    for i in constr:
        if i == True:
            continue  # ignore
        if i == False:
            return  # no solution
        if i.has(S.Infinity, S.NegativeInfinity):
            raise ValueError("only finite bounds are permitted")
        if isinstance(i, (Le, Ge)):
            i = i.lts - i.gts
            freei = i.free_symbols
            if freei - syms:
                raise ValueError(
                    "unexpected symbol(s) in constraint: %s" % (freei - syms)
                )
            if len(freei) > 1:
                np.append(i)
            elif freei:
                x = freei.pop()
                if x in unbound:
                    continue  # will handle later
                ivl = Le(i, 0, evaluate=False).as_set()
                if x not in univariate:
                    univariate[x] = ivl
                else:
                    univariate[x] &= ivl
            elif i:
                return False
        else:
            raise TypeError(filldedent("""
                only equalities like Eq(x, y) or non-strict
                inequalities like x >= y are allowed in lp, not %s""" % i))

    # introduce auxilliary variables as needed for univariate
    # inequalities
    for x in syms:
        i = univariate.get(x, True)
        if not i:
            return None  # no solution possible
        if i == True:
            unbound.append(x)
            continue
        a, b = i.inf, i.sup
        if a.is_infinite:
            u = next(ui)
            r[x] = b - u
            aux.append(u)
        elif b.is_infinite:
            if a:
                u = next(ui)
                r[x] = a + u
                aux.append(u)
            else:
                # standard nonnegative relationship
                pass
        else:
            u = next(ui)
            aux.append(u)
            # shift so u = x - a => x = u + a
            r[x] = u + a
            # add constraint for u <= b - a
            # since when u = b-a then x = u + a = b - a + a = b:
            # the upper limit for x
            np.append(u - (b - a))

    # make change of variables for unbound variables
    for x in unbound:
        u = next(ui)
        r[x] = u - x  # reusing x
        aux.append(u)

    return np, r, aux

