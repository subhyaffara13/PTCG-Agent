
def continuous_domain(f, symbol, domain):
    """
    Returns the domain on which the function expression f is continuous.

    This function is limited by the ability to determine the various
    singularities and discontinuities of the given function.
    The result is either given as a union of intervals or constructed using
    other set operations.

    Parameters
    ==========

    f : :py:class:`~.Expr`
        The concerned function.
    symbol : :py:class:`~.Symbol`
        The variable for which the intervals are to be determined.
    domain : :py:class:`~.Interval`
        The domain over which the continuity of the symbol has to be checked.

    Examples
    ========

    >>> from sympy import Interval, Symbol, S, tan, log, pi, sqrt
    >>> from sympy.calculus.util import continuous_domain
    >>> x = Symbol('x')
    >>> continuous_domain(1/x, x, S.Reals)
    Union(Interval.open(-oo, 0), Interval.open(0, oo))
    >>> continuous_domain(tan(x), x, Interval(0, pi))
    Union(Interval.Ropen(0, pi/2), Interval.Lopen(pi/2, pi))
    >>> continuous_domain(sqrt(x - 2), x, Interval(-5, 5))
    Interval(2, 5)
    >>> continuous_domain(log(2*x - 1), x, S.Reals)
    Interval.open(1/2, oo)

    Returns
    =======

    :py:class:`~.Interval`
        Union of all intervals where the function is continuous.

    Raises
    ======

    NotImplementedError
        If the method to determine continuity of such a function
        has not yet been developed.

    """
    from sympy.solvers.inequalities import solve_univariate_inequality

    if not domain.is_subset(S.Reals):
        raise NotImplementedError(filldedent('''
            Domain must be a subset of S.Reals.
            '''))
    implemented = [Pow, exp, log, Abs, frac,
                   sin, cos, tan, cot, sec, csc,
                   asin, acos, atan, acot, asec, acsc,
                   sinh, cosh, tanh, coth, sech, csch,
                   asinh, acosh, atanh, acoth, asech, acsch]
    used = [fct.func for fct in f.atoms(Function) if fct.has(symbol)]
    if any(func not in implemented for func in used):
        raise NotImplementedError(filldedent('''
            Unable to determine the domain of the given function.
            '''))

    x = Symbol('x')
    constraints = {
        log: (x > 0,),
        asin: (x >= -1, x <= 1),
        acos: (x >= -1, x <= 1),
        acosh: (x >= 1,),
        atanh: (x > -1, x < 1),
        asech: (x > 0, x <= 1)
    }
    constraints_union = {
        asec: (x <= -1, x >= 1),
        acsc: (x <= -1, x >= 1),
        acoth: (x < -1, x > 1)
    }

    cont_domain = domain
    for atom in f.atoms(Pow):
        den = atom.exp.as_numer_denom()[1]
        if atom.exp.is_rational and den.is_odd:
            pass    # 0**negative handled by singularities()
        else:
            constraint = solve_univariate_inequality(atom.base >= 0,
                                                        symbol).as_set()
            cont_domain = Intersection(constraint, cont_domain)

    for atom in f.atoms(Function):
        if atom.func in constraints:
            for c in constraints[atom.func]:
                constraint_relational = c.subs(x, atom.args[0])
                constraint_set = solve_univariate_inequality(
                    constraint_relational, symbol).as_set()
                cont_domain = Intersection(constraint_set, cont_domain)
        elif atom.func in constraints_union:
            constraint_set = S.EmptySet
            for c in constraints_union[atom.func]:
                constraint_relational = c.subs(x, atom.args[0])
                constraint_set += solve_univariate_inequality(
                    constraint_relational, symbol).as_set()
            cont_domain = Intersection(constraint_set, cont_domain)
        # XXX: the discontinuities below could be factored out in
        # a new "discontinuities()".
        elif atom.func == acot:
            from sympy.solvers.solveset import solveset_real
            # Sympy's acot() has a step discontinuity at 0. Since it's
            # neither an essential singularity nor a pole, singularities()
            # will not report it. But it's still relevant for determining
            # the continuity of the function f.
            cont_domain -= solveset_real(atom.args[0], symbol)
            # Note that the above may introduce spurious discontinuities, e.g.
            # for abs(acot(x)) at 0.
        elif atom.func == frac:
            from sympy.solvers.solveset import solveset_real
            r = function_range(atom.args[0], symbol, domain)
            r = Intersection(r, S.Integers)
            if r.is_finite_set:
                discont = S.EmptySet
                for n in r:
                    discont += solveset_real(atom.args[0]-n, symbol)
            else:
                discont = ConditionSet(
                    symbol, S.Integers.contains(atom.args[0]), cont_domain)
            cont_domain -= discont

    return cont_domain - singularities(f, symbol, domain)

