import re
from typing import Union

def _solveset(f, symbol, domain, _check=False):
    """Helper for solveset to return a result from an expression
    that has already been sympify'ed and is known to contain the
    given symbol."""
    # _check controls whether the answer is checked or not
    from sympy.simplify.simplify import signsimp

    if isinstance(f, BooleanTrue):
        return domain

    orig_f = f
    if f.is_Mul:
        coeff, f = f.as_independent(symbol, as_Add=False)
        if coeff in {S.ComplexInfinity, S.NegativeInfinity, S.Infinity}:
            f = together(orig_f)
    elif f.is_Add:
        a, h = f.as_independent(symbol)
        m, h = h.as_independent(symbol, as_Add=False)
        if m not in {S.ComplexInfinity, S.Zero, S.Infinity,
                              S.NegativeInfinity}:
            f = a/m + h  # XXX condition `m != 0` should be added to soln

    # assign the solvers to use
    solver = lambda f, x, domain=domain: _solveset(f, x, domain)
    inverter = lambda f, rhs, symbol: _invert(f, rhs, symbol, domain)

    result = S.EmptySet

    if f.expand().is_zero:
        return domain
    elif not f.has(symbol):
        return S.EmptySet
    elif f.is_Mul and all(_is_finite_with_finite_vars(m, domain)
            for m in f.args):
        # if f(x) and g(x) are both finite we can say that the solution of
        # f(x)*g(x) == 0 is same as Union(f(x) == 0, g(x) == 0) is not true in
        # general. g(x) can grow to infinitely large for the values where
        # f(x) == 0. To be sure that we are not silently allowing any
        # wrong solutions we are using this technique only if both f and g are
        # finite for a finite input.
        result = Union(*[solver(m, symbol) for m in f.args])
    elif (_is_function_class_equation(TrigonometricFunction, f, symbol) or \
            _is_function_class_equation(HyperbolicFunction, f, symbol)):
        result = _solve_trig(f, symbol, domain)
    elif isinstance(f, arg):
        a = f.args[0]
        result = Intersection(_solveset(re(a) > 0, symbol, domain),
                              _solveset(im(a), symbol, domain))
    elif f.is_Piecewise:
        expr_set_pairs = f.as_expr_set_pairs(domain)
        for (expr, in_set) in expr_set_pairs:
            if in_set.is_Relational:
                in_set = in_set.as_set()
            solns = solver(expr, symbol, in_set)
            result += solns
    elif isinstance(f, Eq):
        result = solver(Add(f.lhs, -f.rhs, evaluate=False), symbol, domain)

    elif f.is_Relational:
        from .inequalities import solve_univariate_inequality
        try:
            result = solve_univariate_inequality(
            f, symbol, domain=domain, relational=False)
        except NotImplementedError:
            result = ConditionSet(symbol, f, domain)
        return result
    elif _is_modular(f, symbol):
        result = _solve_modular(f, symbol, domain)
    else:
        lhs, rhs_s = inverter(f, 0, symbol)
        if lhs == symbol:
            # do some very minimal simplification since
            # repeated inversion may have left the result
            # in a state that other solvers (e.g. poly)
            # would have simplified; this is done here
            # rather than in the inverter since here it
            # is only done once whereas there it would
            # be repeated for each step of the inversion
            if isinstance(rhs_s, FiniteSet):
                rhs_s = FiniteSet(*[Mul(*
                    signsimp(i).as_content_primitive())
                    for i in rhs_s])
            result = rhs_s

        elif isinstance(rhs_s, FiniteSet):
            for equation in [lhs - rhs for rhs in rhs_s]:
                if equation == f:
                    u = unrad(f, symbol)
                    if u:
                        result += _solve_radical(equation, u,
                                                 symbol,
                                                 solver)
                    elif equation.has(Abs):
                        result += _solve_abs(f, symbol, domain)
                    else:
                        result_rational = _solve_as_rational(equation, symbol, domain)
                        if not isinstance(result_rational, ConditionSet):
                            result += result_rational
                        else:
                            # may be a transcendental type equation
                            t_result = _transolve(equation, symbol, domain)
                            if isinstance(t_result, ConditionSet):
                                # might need factoring; this is expensive so we
                                # have delayed until now. To avoid recursion
                                # errors look for a non-trivial factoring into
                                # a product of symbol dependent terms; I think
                                # that something that factors as a Pow would
                                # have already been recognized by now.
                                factored = equation.factor()
                                if factored.is_Mul and equation != factored:
                                    _, dep = factored.as_independent(symbol)
                                    if not dep.is_Add:
                                        # non-trivial factoring of equation
                                        # but use form with constants
                                        # in case they need special handling
                                        t_results = []
                                        for fac in Mul.make_args(factored):
                                            if fac.has(symbol):
                                                t_results.append(solver(fac, symbol))
                                        t_result = Union(*t_results)
                            result += t_result
                else:
                    result += solver(equation, symbol)

        elif rhs_s is not S.EmptySet:
            result = ConditionSet(symbol, Eq(f, 0), domain)

    if isinstance(result, ConditionSet):
        if isinstance(f, Expr):
            num, den = f.as_numer_denom()
            if den.has(symbol):
                _result = _solveset(num, symbol, domain)
                if not isinstance(_result, ConditionSet):
                    singularities = _solveset(den, symbol, domain)
                    result = _result - singularities

    if _check:
        if isinstance(result, ConditionSet):
            # it wasn't solved or has enumerated all conditions
            # -- leave it alone
            return result

        # whittle away all but the symbol-containing core
        # to use this for testing
        if isinstance(orig_f, Expr):
            fx = orig_f.as_independent(symbol, as_Add=True)[1]
            fx = fx.as_independent(symbol, as_Add=False)[1]
        else:
            fx = orig_f

        if isinstance(result, FiniteSet):
            # check the result for invalid solutions
            result = FiniteSet(*[s for s in result
                      if isinstance(s, RootOf)
                      or domain_check(fx, symbol, s)])

    return result

