
def nsolve(*args, dict=False, **kwargs):
    r"""
    Solve a nonlinear equation system numerically: ``nsolve(f, [args,] x0,
    modules=['mpmath'], **kwargs)``.

    Explanation
    ===========

    ``f`` is a vector function of symbolic expressions representing the system.
    *args* are the variables. If there is only one variable, this argument can
    be omitted. ``x0`` is a starting vector close to a solution.

    Use the modules keyword to specify which modules should be used to
    evaluate the function and the Jacobian matrix. Make sure to use a module
    that supports matrices. For more information on the syntax, please see the
    docstring of ``lambdify``.

    If the keyword arguments contain ``dict=True`` (default is False) ``nsolve``
    will return a list (perhaps empty) of solution mappings. This might be
    especially useful if you want to use ``nsolve`` as a fallback to solve since
    using the dict argument for both methods produces return values of
    consistent type structure. Please note: to keep this consistent with
    ``solve``, the solution will be returned in a list even though ``nsolve``
    (currently at least) only finds one solution at a time.

    Overdetermined systems are supported.

    Examples
    ========

    >>> from sympy import Symbol, nsolve
    >>> import mpmath
    >>> mpmath.mp.dps = 15
    >>> x1 = Symbol('x1')
    >>> x2 = Symbol('x2')
    >>> f1 = 3 * x1**2 - 2 * x2**2 - 1
    >>> f2 = x1**2 - 2 * x1 + x2**2 + 2 * x2 - 8
    >>> print(nsolve((f1, f2), (x1, x2), (-1, 1)))
    Matrix([[-1.19287309935246], [1.27844411169911]])

    For one-dimensional functions the syntax is simplified:

    >>> from sympy import sin, nsolve
    >>> from sympy.abc import x
    >>> nsolve(sin(x), x, 2)
    3.14159265358979
    >>> nsolve(sin(x), 2)
    3.14159265358979

    To solve with higher precision than the default, use the prec argument:

    >>> from sympy import cos
    >>> nsolve(cos(x) - x, 1)
    0.739085133215161
    >>> nsolve(cos(x) - x, 1, prec=50)
    0.73908513321516064165531208767387340401341175890076
    >>> cos(_)
    0.73908513321516064165531208767387340401341175890076

    To solve for complex roots of real functions, a nonreal initial point
    must be specified:

    >>> from sympy import I
    >>> nsolve(x**2 + 2, I)
    1.4142135623731*I

    ``mpmath.findroot`` is used and you can find their more extensive
    documentation, especially concerning keyword parameters and
    available solvers. Note, however, that functions which are very
    steep near the root, the verification of the solution may fail. In
    this case you should use the flag ``verify=False`` and
    independently verify the solution.

    >>> from sympy import cos, cosh
    >>> f = cos(x)*cosh(x) - 1
    >>> nsolve(f, 3.14*100)
    Traceback (most recent call last):
    ...
    ValueError: Could not find root within given tolerance. (1.39267e+230 > 2.1684e-19)
    >>> ans = nsolve(f, 3.14*100, verify=False); ans
    312.588469032184
    >>> f.subs(x, ans).n(2)
    2.1e+121
    >>> (f/f.diff(x)).subs(x, ans).n(2)
    7.4e-15

    One might safely skip the verification if bounds of the root are known
    and a bisection method is used:

    >>> bounds = lambda i: (3.14*i, 3.14*(i + 1))
    >>> nsolve(f, bounds(100), solver='bisect', verify=False)
    315.730061685774

    Alternatively, a function may be better behaved when the
    denominator is ignored. Since this is not always the case, however,
    the decision of what function to use is left to the discretion of
    the user.

    >>> eq = x**2/(1 - x)/(1 - 2*x)**2 - 100
    >>> nsolve(eq, 0.46)
    Traceback (most recent call last):
    ...
    ValueError: Could not find root within given tolerance. (10000 > 2.1684e-19)
    Try another starting point or tweak arguments.
    >>> nsolve(eq.as_numer_denom()[0], 0.46)
    0.46792545969349058

    """
    # there are several other SymPy functions that use method= so
    # guard against that here
    if 'method' in kwargs:
        raise ValueError(filldedent('''
            Keyword "method" should not be used in this context.  When using
            some mpmath solvers directly, the keyword "method" is
            used, but when using nsolve (and findroot) the keyword to use is
            "solver".'''))

    if 'prec' in kwargs:
        import mpmath
        mpmath.mp.dps = kwargs.pop('prec')

    # keyword argument to return result as a dictionary
    as_dict = dict
    from builtins import dict  # to unhide the builtin

    # interpret arguments
    if len(args) == 3:
        f = args[0]
        fargs = args[1]
        x0 = args[2]
        if iterable(fargs) and iterable(x0):
            if len(x0) != len(fargs):
                raise TypeError('nsolve expected exactly %i guess vectors, got %i'
                                % (len(fargs), len(x0)))
    elif len(args) == 2:
        f = args[0]
        fargs = None
        x0 = args[1]
        if iterable(f):
            raise TypeError('nsolve expected 3 arguments, got 2')
    elif len(args) < 2:
        raise TypeError('nsolve expected at least 2 arguments, got %i'
                        % len(args))
    else:
        raise TypeError('nsolve expected at most 3 arguments, got %i'
                        % len(args))
    modules = kwargs.get('modules', ['mpmath'])
    if iterable(f):
        f = list(f)
        for i, fi in enumerate(f):
            if isinstance(fi, Eq):
                f[i] = fi.lhs - fi.rhs
        f = Matrix(f).T
    if iterable(x0):
        x0 = list(x0)
    if not isinstance(f, Matrix):
        # assume it's a SymPy expression
        if isinstance(f, Eq):
            f = f.lhs - f.rhs
        elif f.is_Relational:
            raise TypeError('nsolve cannot accept inequalities')
        syms = f.free_symbols
        if fargs is None:
            fargs = syms.copy().pop()
        if not (len(syms) == 1 and (fargs in syms or fargs[0] in syms)):
            raise ValueError(filldedent('''
                expected a one-dimensional and numerical function'''))

        # the function is much better behaved if there is no denominator
        # but sending the numerator is left to the user since sometimes
        # the function is better behaved when the denominator is present
        # e.g., issue 11768

        f = lambdify(fargs, f, modules)
        x = sympify(findroot(f, x0, **kwargs))
        if as_dict:
            return [{fargs: x}]
        return x

    if len(fargs) > f.cols:
        raise NotImplementedError(filldedent('''
            need at least as many equations as variables'''))
    verbose = kwargs.get('verbose', False)
    if verbose:
        print('f(x):')
        print(f)
    # derive Jacobian
    J = f.jacobian(fargs)
    if verbose:
        print('J(x):')
        print(J)
    # create functions
    f = lambdify(fargs, f.T, modules)
    J = lambdify(fargs, J, modules)
    # solve the system numerically
    x = findroot(f, x0, J=J, **kwargs)
    if as_dict:
        return [dict(zip(fargs, [sympify(xi) for xi in x]))]
    return Matrix(x)

