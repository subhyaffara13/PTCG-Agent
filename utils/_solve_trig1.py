from typing import Union

def _solve_trig1(f, symbol, domain):
    """Primary solver for trigonometric and hyperbolic equations

    Returns either the solution set as a ConditionSet (auto-evaluated to a
    union of ImageSets if no variables besides 'symbol' are involved) or
    raises _SolveTrig1Error if f == 0 cannot be solved.

    Notes
    =====
    Algorithm:
    1. Do a change of variable x -> mu*x in arguments to trigonometric and
    hyperbolic functions, in order to reduce them to small integers. (This
    step is crucial to keep the degrees of the polynomials of step 4 low.)
    2. Rewrite trigonometric/hyperbolic functions as exponentials.
    3. Proceed to a 2nd change of variable, replacing exp(I*x) or exp(x) by y.
    4. Solve the resulting rational equation.
    5. Use invert_complex or invert_real to return to the original variable.
    6. If the coefficients of 'symbol' were symbolic in nature, add the
    necessary consistency conditions in a ConditionSet.

    """
    # Prepare change of variable
    x = Dummy('x')
    if _is_function_class_equation(HyperbolicFunction, f, symbol):
        cov = exp(x)
        inverter = invert_real if domain.is_subset(S.Reals) else invert_complex
    else:
        cov = exp(I*x)
        inverter = invert_complex

    f = trigsimp(f)
    f_original = f
    trig_functions = f.atoms(TrigonometricFunction, HyperbolicFunction)
    trig_arguments = [e.args[0] for e in trig_functions]
    # trigsimp may have reduced the equation to an expression
    # that is independent of 'symbol' (e.g. cos**2+sin**2)
    if not any(a.has(symbol) for a in trig_arguments):
        return solveset(f_original, symbol, domain)

    denominators = []
    numerators = []
    for ar in trig_arguments:
        try:
            poly_ar = Poly(ar, symbol)
        except PolynomialError:
            raise _SolveTrig1Error("trig argument is not a polynomial")
        if poly_ar.degree() > 1:  # degree >1 still bad
            raise _SolveTrig1Error("degree of variable must not exceed one")
        if poly_ar.degree() == 0:  # degree 0, don't care
            continue
        c = poly_ar.all_coeffs()[0]   # got the coefficient of 'symbol'
        numerators.append(fraction(c)[0])
        denominators.append(fraction(c)[1])

    mu = lcm(denominators)/gcd(numerators)
    f = f.subs(symbol, mu*x)
    f = f.rewrite(exp)
    f = together(f)
    g, h = fraction(f)
    y = Dummy('y')
    g, h = g.expand(), h.expand()
    g, h = g.subs(cov, y), h.subs(cov, y)
    if g.has(x) or h.has(x):
        raise _SolveTrig1Error("change of variable not possible")

    solns = solveset_complex(g, y) - solveset_complex(h, y)
    if isinstance(solns, ConditionSet):
        raise _SolveTrig1Error("polynomial has ConditionSet solution")

    if isinstance(solns, FiniteSet):
        if any(isinstance(s, RootOf) for s in solns):
            raise _SolveTrig1Error("polynomial results in RootOf object")
        # revert the change of variable
        cov = cov.subs(x, symbol/mu)
        result = Union(*[inverter(cov, s, symbol)[1] for s in solns])
        # In case of symbolic coefficients, the solution set is only valid
        # if numerator and denominator of mu are non-zero.
        if mu.has(Symbol):
            syms = (mu).atoms(Symbol)
            munum, muden = fraction(mu)
            condnum = munum.as_independent(*syms, as_Add=False)[1]
            condden = muden.as_independent(*syms, as_Add=False)[1]
            cond = And(Ne(condnum, 0), Ne(condden, 0))
        else:
            cond = True
        # Actual conditions are returned as part of the ConditionSet. Adding an
        # intersection with C would only complicate some solution sets due to
        # current limitations of intersection code. (e.g. #19154)
        if domain is S.Complexes:
            # This is a slight abuse of ConditionSet. Ideally this should
            # be some kind of "PiecewiseSet". (See #19507 discussion)
            return ConditionSet(symbol, cond, result)
        else:
            return ConditionSet(symbol, cond, Intersection(result, domain))
    elif solns is S.EmptySet:
        return S.EmptySet
    else:
        raise _SolveTrig1Error("polynomial solutions must form FiniteSet")

