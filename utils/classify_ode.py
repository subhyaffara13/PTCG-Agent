
def classify_ode(eq, func=None, dict=False, ics=None, *, prep=True, xi=None, eta=None, n=None, **kwargs):
    r"""
    Returns a tuple of possible :py:meth:`~sympy.solvers.ode.dsolve`
    classifications for an ODE.

    The tuple is ordered so that first item is the classification that
    :py:meth:`~sympy.solvers.ode.dsolve` uses to solve the ODE by default.  In
    general, classifications at the near the beginning of the list will
    produce better solutions faster than those near the end, thought there are
    always exceptions.  To make :py:meth:`~sympy.solvers.ode.dsolve` use a
    different classification, use ``dsolve(ODE, func,
    hint=<classification>)``.  See also the
    :py:meth:`~sympy.solvers.ode.dsolve` docstring for different meta-hints
    you can use.

    If ``dict`` is true, :py:meth:`~sympy.solvers.ode.classify_ode` will
    return a dictionary of ``hint:match`` expression terms. This is intended
    for internal use by :py:meth:`~sympy.solvers.ode.dsolve`.  Note that
    because dictionaries are ordered arbitrarily, this will most likely not be
    in the same order as the tuple.

    You can get help on different hints by executing
    ``help(ode.ode_hintname)``, where ``hintname`` is the name of the hint
    without ``_Integral``.

    See :py:data:`~sympy.solvers.ode.allhints` or the
    :py:mod:`~sympy.solvers.ode` docstring for a list of all supported hints
    that can be returned from :py:meth:`~sympy.solvers.ode.classify_ode`.

    Notes
    =====

    These are remarks on hint names.

    ``_Integral``

        If a classification has ``_Integral`` at the end, it will return the
        expression with an unevaluated :py:class:`~.Integral`
        class in it.  Note that a hint may do this anyway if
        :py:meth:`~sympy.core.expr.Expr.integrate` cannot do the integral,
        though just using an ``_Integral`` will do so much faster.  Indeed, an
        ``_Integral`` hint will always be faster than its corresponding hint
        without ``_Integral`` because
        :py:meth:`~sympy.core.expr.Expr.integrate` is an expensive routine.
        If :py:meth:`~sympy.solvers.ode.dsolve` hangs, it is probably because
        :py:meth:`~sympy.core.expr.Expr.integrate` is hanging on a tough or
        impossible integral.  Try using an ``_Integral`` hint or
        ``all_Integral`` to get it return something.

        Note that some hints do not have ``_Integral`` counterparts. This is
        because :py:func:`~sympy.integrals.integrals.integrate` is not used in
        solving the ODE for those method. For example, `n`\th order linear
        homogeneous ODEs with constant coefficients do not require integration
        to solve, so there is no
        ``nth_linear_homogeneous_constant_coeff_Integrate`` hint. You can
        easily evaluate any unevaluated
        :py:class:`~sympy.integrals.integrals.Integral`\s in an expression by
        doing ``expr.doit()``.

    Ordinals

        Some hints contain an ordinal such as ``1st_linear``.  This is to help
        differentiate them from other hints, as well as from other methods
        that may not be implemented yet. If a hint has ``nth`` in it, such as
        the ``nth_linear`` hints, this means that the method used to applies
        to ODEs of any order.

    ``indep`` and ``dep``

        Some hints contain the words ``indep`` or ``dep``.  These reference
        the independent variable and the dependent function, respectively. For
        example, if an ODE is in terms of `f(x)`, then ``indep`` will refer to
        `x` and ``dep`` will refer to `f`.

    ``subs``

        If a hints has the word ``subs`` in it, it means that the ODE is solved
        by substituting the expression given after the word ``subs`` for a
        single dummy variable.  This is usually in terms of ``indep`` and
        ``dep`` as above.  The substituted expression will be written only in
        characters allowed for names of Python objects, meaning operators will
        be spelled out.  For example, ``indep``/``dep`` will be written as
        ``indep_div_dep``.

    ``coeff``

        The word ``coeff`` in a hint refers to the coefficients of something
        in the ODE, usually of the derivative terms.  See the docstring for
        the individual methods for more info (``help(ode)``).  This is
        contrast to ``coefficients``, as in ``undetermined_coefficients``,
        which refers to the common name of a method.

    ``_best``

        Methods that have more than one fundamental way to solve will have a
        hint for each sub-method and a ``_best`` meta-classification. This
        will evaluate all hints and return the best, using the same
        considerations as the normal ``best`` meta-hint.


    Examples
    ========

    >>> from sympy import Function, classify_ode, Eq
    >>> from sympy.abc import x
    >>> f = Function('f')
    >>> classify_ode(Eq(f(x).diff(x), 0), f(x))
    ('nth_algebraic',
    'separable',
    '1st_exact',
    '1st_linear',
    'Bernoulli',
    '1st_homogeneous_coeff_best',
    '1st_homogeneous_coeff_subs_indep_div_dep',
    '1st_homogeneous_coeff_subs_dep_div_indep',
    '1st_power_series', 'lie_group', 'nth_linear_constant_coeff_homogeneous',
    'nth_linear_euler_eq_homogeneous',
    'nth_algebraic_Integral', 'separable_Integral', '1st_exact_Integral',
    '1st_linear_Integral', 'Bernoulli_Integral',
    '1st_homogeneous_coeff_subs_indep_div_dep_Integral',
    '1st_homogeneous_coeff_subs_dep_div_indep_Integral')
    >>> classify_ode(f(x).diff(x, 2) + 3*f(x).diff(x) + 2*f(x) - 4)
    ('factorable', 'nth_linear_constant_coeff_undetermined_coefficients',
    'nth_linear_constant_coeff_variation_of_parameters',
    'nth_linear_constant_coeff_variation_of_parameters_Integral')

    """
    ics = sympify(ics)

    if func and len(func.args) != 1:
        raise ValueError("dsolve() and classify_ode() only "
        "work with functions of one variable, not %s" % func)

    if isinstance(eq, Equality):
        eq = eq.lhs - eq.rhs

    # Some methods want the unprocessed equation
    eq_orig = eq

    if prep or func is None:
        eq, func_ = _preprocess(eq, func)
        if func is None:
            func = func_
    x = func.args[0]
    f = func.func
    y = Dummy('y')
    terms = 5 if n is None else n

    order = ode_order(eq, f(x))
    # hint:matchdict or hint:(tuple of matchdicts)
    # Also will contain "default":<default hint> and "order":order items.
    matching_hints = {"order": order}

    df = f(x).diff(x)
    a = Wild('a', exclude=[f(x)])
    d = Wild('d', exclude=[df, f(x).diff(x, 2)])
    e = Wild('e', exclude=[df])
    n = Wild('n', exclude=[x, f(x), df])
    c1 = Wild('c1', exclude=[x])
    a3 = Wild('a3', exclude=[f(x), df, f(x).diff(x, 2)])
    b3 = Wild('b3', exclude=[f(x), df, f(x).diff(x, 2)])
    c3 = Wild('c3', exclude=[f(x), df, f(x).diff(x, 2)])
    boundary = {}  # Used to extract initial conditions
    C1 = Symbol("C1")

    # Preprocessing to get the initial conditions out
    if ics is not None:
        for funcarg in ics:
            # Separating derivatives
            if isinstance(funcarg, (Subs, Derivative)):
                # f(x).diff(x).subs(x, 0) is a Subs, but f(x).diff(x).subs(x,
                # y) is a Derivative
                if isinstance(funcarg, Subs):
                    deriv = funcarg.expr
                    old = funcarg.variables[0]
                    new = funcarg.point[0]
                elif isinstance(funcarg, Derivative):
                    deriv = funcarg
                    # No information on this. Just assume it was x
                    old = x
                    new = funcarg.variables[0]

                if (isinstance(deriv, Derivative) and isinstance(deriv.args[0],
                    AppliedUndef) and deriv.args[0].func == f and
                    len(deriv.args[0].args) == 1 and old == x and not
                    new.has(x) and all(i == deriv.variables[0] for i in
                    deriv.variables) and x not in ics[funcarg].free_symbols):

                    dorder = ode_order(deriv, x)
                    temp = 'f' + str(dorder)
                    boundary.update({temp: new, temp + 'val': ics[funcarg]})
                else:
                    raise ValueError("Invalid boundary conditions for Derivatives")


            # Separating functions
            elif isinstance(funcarg, AppliedUndef):
                if (funcarg.func == f and len(funcarg.args) == 1 and
                    not funcarg.args[0].has(x) and x not in ics[funcarg].free_symbols):
                    boundary.update({'f0': funcarg.args[0], 'f0val': ics[funcarg]})
                else:
                    raise ValueError("Invalid boundary conditions for Function")

            else:
                raise ValueError("Enter boundary conditions of the form ics={f(point): value, f(x).diff(x, order).subs(x, point): value}")

    ode = SingleODEProblem(eq_orig, func, x, prep=prep, xi=xi, eta=eta)
    user_hint = kwargs.get('hint', 'default')
    # Used when dsolve is called without an explicit hint.
    # We exit early to return the first valid match
    early_exit = (user_hint=='default')
    user_hint = user_hint.removesuffix('_Integral')
    user_map = solver_map
    # An explicit hint has been given to dsolve
    # Skip matching code for other hints
    if user_hint not in ['default', 'all', 'all_Integral', 'best'] and user_hint in solver_map:
        user_map = {user_hint: solver_map[user_hint]}

    for hint in user_map:
        solver = user_map[hint](ode)
        if solver.matches():
            matching_hints[hint] = solver
            if user_map[hint].has_integral:
                matching_hints[hint + "_Integral"] = solver
            if dict and early_exit:
                matching_hints["default"] = hint
                return matching_hints

    eq = expand(eq)
    # Precondition to try remove f(x) from highest order derivative
    reduced_eq = None
    if eq.is_Add:
        deriv_coef = eq.coeff(f(x).diff(x, order))
        if deriv_coef not in (1, 0):
            r = deriv_coef.match(a*f(x)**c1)
            if r and r[c1]:
                den = f(x)**r[c1]
                reduced_eq = Add(*[arg/den for arg in eq.args])
    if not reduced_eq:
        reduced_eq = eq

    if order == 1:

        # NON-REDUCED FORM OF EQUATION matches
        r = collect(eq, df, exact=True).match(d + e * df)
        if r:
            r['d'] = d
            r['e'] = e
            r['y'] = y
            r[d] = r[d].subs(f(x), y)
            r[e] = r[e].subs(f(x), y)

            # FIRST ORDER POWER SERIES WHICH NEEDS INITIAL CONDITIONS
            # TODO: Hint first order series should match only if d/e is analytic.
            # For now, only d/e and (d/e).diff(arg) is checked for existence at
            # at a given point.
            # This is currently done internally in ode_1st_power_series.
            point = boundary.get('f0', 0)
            value = boundary.get('f0val', C1)
            check = cancel(r[d]/r[e])
            check1 = check.subs({x: point, y: value})
            if not check1.has(oo) and not check1.has(zoo) and \
                not check1.has(nan) and not check1.has(-oo):
                check2 = (check1.diff(x)).subs({x: point, y: value})
                if not check2.has(oo) and not check2.has(zoo) and \
                    not check2.has(nan) and not check2.has(-oo):
                    rseries = r.copy()
                    rseries.update({'terms': terms, 'f0': point, 'f0val': value})
                    matching_hints["1st_power_series"] = rseries

    elif order == 2:
        # Homogeneous second order differential equation of the form
        # a3*f(x).diff(x, 2) + b3*f(x).diff(x) + c3
        # It has a definite power series solution at point x0 if, b3/a3 and c3/a3
        # are analytic at x0.
        deq = a3*(f(x).diff(x, 2)) + b3*df + c3*f(x)
        r = collect(reduced_eq,
            [f(x).diff(x, 2), f(x).diff(x), f(x)]).match(deq)
        ordinary = False
        if r:
            if not all(r[key].is_polynomial() for key in r):
                n, d = reduced_eq.as_numer_denom()
                reduced_eq = expand(n)
                r = collect(reduced_eq,
                    [f(x).diff(x, 2), f(x).diff(x), f(x)]).match(deq)
        if r and r[a3] != 0:
            p = cancel(r[b3]/r[a3])  # Used below
            q = cancel(r[c3]/r[a3])  # Used below
            point = kwargs.get('x0', 0)
            check = p.subs(x, point)
            if not check.has(oo, nan, zoo, -oo):
                check = q.subs(x, point)
                if not check.has(oo, nan, zoo, -oo):
                    ordinary = True
                    r.update({'a3': a3, 'b3': b3, 'c3': c3, 'x0': point, 'terms': terms})
                    matching_hints["2nd_power_series_ordinary"] = r

            # Checking if the differential equation has a regular singular point
            # at x0. It has a regular singular point at x0, if (b3/a3)*(x - x0)
            # and (c3/a3)*((x - x0)**2) are analytic at x0.
            if not ordinary:
                p = cancel((x - point)*p)
                check = p.subs(x, point)
                if not check.has(oo, nan, zoo, -oo):
                    q = cancel(((x - point)**2)*q)
                    check = q.subs(x, point)
                    if not check.has(oo, nan, zoo, -oo):
                        coeff_dict = {'p': p, 'q': q, 'x0': point, 'terms': terms}
                        matching_hints["2nd_power_series_regular"] = coeff_dict


    # Order keys based on allhints.
    retlist = [i for i in allhints if i in matching_hints]
    if dict:
        # Dictionaries are ordered arbitrarily, so make note of which
        # hint would come first for dsolve().  Use an ordered dict in Py 3.
        matching_hints["default"] = retlist[0] if retlist else None
        matching_hints["ordered_hints"] = tuple(retlist)
        return matching_hints
    else:
        return tuple(retlist)

