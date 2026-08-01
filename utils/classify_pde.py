
def classify_pde(eq, func=None, dict=False, *, prep=True, **kwargs):
    """
    Returns a tuple of possible pdsolve() classifications for a PDE.

    The tuple is ordered so that first item is the classification that
    pdsolve() uses to solve the PDE by default.  In general,
    classifications near the beginning of the list will produce
    better solutions faster than those near the end, though there are
    always exceptions.  To make pdsolve use a different classification,
    use pdsolve(PDE, func, hint=<classification>).  See also the pdsolve()
    docstring for different meta-hints you can use.

    If ``dict`` is true, classify_pde() will return a dictionary of
    hint:match expression terms. This is intended for internal use by
    pdsolve().  Note that because dictionaries are ordered arbitrarily,
    this will most likely not be in the same order as the tuple.

    You can get help on different hints by doing help(pde.pde_hintname),
    where hintname is the name of the hint without "_Integral".

    See sympy.pde.allhints or the sympy.pde docstring for a list of all
    supported hints that can be returned from classify_pde.


    Examples
    ========

    >>> from sympy.solvers.pde import classify_pde
    >>> from sympy import Function, Eq
    >>> from sympy.abc import x, y
    >>> f = Function('f')
    >>> u = f(x, y)
    >>> ux = u.diff(x)
    >>> uy = u.diff(y)
    >>> eq = Eq(1 + (2*(ux/u)) + (3*(uy/u)), 0)
    >>> classify_pde(eq)
    ('1st_linear_constant_coeff_homogeneous',)
    """

    if func and len(func.args) != 2:
        raise NotImplementedError("Right now only partial "
            "differential equations of two variables are supported")

    if prep or func is None:
        prep, func_ = _preprocess(eq, func)
        if func is None:
            func = func_

    if isinstance(eq, Equality):
        if eq.rhs != 0:
            return classify_pde(eq.lhs - eq.rhs, func)
        eq = eq.lhs

    f = func.func
    x = func.args[0]
    y = func.args[1]
    fx = f(x,y).diff(x)
    fy = f(x,y).diff(y)

    # TODO : For now pde.py uses support offered by the ode_order function
    # to find the order with respect to a multi-variable function. An
    # improvement could be to classify the order of the PDE on the basis of
    # individual variables.
    order = ode_order(eq, f(x,y))

    # hint:matchdict or hint:(tuple of matchdicts)
    # Also will contain "default":<default hint> and "order":order items.
    matching_hints = {'order': order}

    if not order:
        if dict:
            matching_hints["default"] = None
            return matching_hints
        return ()

    eq = expand(eq)

    a = Wild('a', exclude = [f(x,y)])
    b = Wild('b', exclude = [f(x,y), fx, fy, x, y])
    c = Wild('c', exclude = [f(x,y), fx, fy, x, y])
    d = Wild('d', exclude = [f(x,y), fx, fy, x, y])
    e = Wild('e', exclude = [f(x,y), fx, fy])
    n = Wild('n', exclude = [x, y])
    # Try removing the smallest power of f(x,y)
    # from the highest partial derivatives of f(x,y)
    reduced_eq = eq
    if eq.is_Add:
        power = None
        for i in set(combinations_with_replacement((x,y), order)):
            coeff = eq.coeff(f(x,y).diff(*i))
            if coeff == 1:
                continue
            match = coeff.match(a*f(x,y)**n)
            if match and match[a]:
                if power is None or match[n] < power:
                    power = match[n]
        if power:
            den = f(x,y)**power
            reduced_eq = Add(*[arg/den for arg in eq.args])

    if order == 1:
        reduced_eq = collect(reduced_eq, f(x, y))
        r = reduced_eq.match(b*fx + c*fy + d*f(x,y) + e)
        if r:
            if not r[e]:
                ## Linear first-order homogeneous partial-differential
                ## equation with constant coefficients
                r.update({'b': b, 'c': c, 'd': d})
                matching_hints["1st_linear_constant_coeff_homogeneous"] = r
            elif r[b]**2 + r[c]**2 != 0:
                ## Linear first-order general partial-differential
                ## equation with constant coefficients
                r.update({'b': b, 'c': c, 'd': d, 'e': e})
                matching_hints["1st_linear_constant_coeff"] = r
                matching_hints["1st_linear_constant_coeff_Integral"] = r

        else:
            b = Wild('b', exclude=[f(x, y), fx, fy])
            c = Wild('c', exclude=[f(x, y), fx, fy])
            d = Wild('d', exclude=[f(x, y), fx, fy])
            r = reduced_eq.match(b*fx + c*fy + d*f(x,y) + e)
            if r:
                r.update({'b': b, 'c': c, 'd': d, 'e': e})
                matching_hints["1st_linear_variable_coeff"] = r

    # Order keys based on allhints.
    rettuple = tuple(i for i in allhints if i in matching_hints)

    if dict:
        # Dictionaries are ordered arbitrarily, so make note of which
        # hint would come first for pdsolve().  Use an ordered dict in Py 3.
        matching_hints["default"] = None
        matching_hints["ordered_hints"] = rettuple
        for i in allhints:
            if i in matching_hints:
                matching_hints["default"] = i
                break
        return matching_hints
    return rettuple

