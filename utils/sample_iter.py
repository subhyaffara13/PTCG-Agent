
def sample_iter(expr, condition=None, size=(), library='scipy',
                    numsamples=S.Infinity, seed=None, **kwargs):

    """
    Returns an iterator of realizations from the expression given a condition.

    Parameters
    ==========

    expr: Expr
        Random expression to be realized
    condition: Expr, optional
        A conditional expression
    size : int, tuple
        Represents size of each sample in numsamples
    numsamples: integer, optional
        Length of the iterator (defaults to infinity)
    seed :
        An object to be used as seed by the given external library for sampling `expr`.
        Following is the list of possible types of object for the supported libraries,

        - 'scipy': int, numpy.random.RandomState, numpy.random.Generator
        - 'numpy': int, numpy.random.RandomState, numpy.random.Generator
        - 'pymc': int

        Optional, by default None, in which case seed settings
        related to the given library will be used.
        No modifications to environment's global seed settings
        are done by this argument.

    Examples
    ========

    >>> from sympy.stats import Normal, sample_iter
    >>> X = Normal('X', 0, 1)
    >>> expr = X*X + 3
    >>> iterator = sample_iter(expr, numsamples=3) # doctest: +SKIP
    >>> list(iterator) # doctest: +SKIP
    [12, 4, 7]

    Returns
    =======

    sample_iter: iterator object
        iterator object containing the sample/samples of given expr

    See Also
    ========

    sample
    sampling_P
    sampling_E

    """
    from sympy.stats.joint_rv import JointRandomSymbol
    if not import_module(library):
        raise ValueError("Failed to import %s" % library)

    if condition is not None:
        ps = pspace(Tuple(expr, condition))
    else:
        ps = pspace(expr)

    rvs = list(ps.values)
    if isinstance(expr, JointRandomSymbol):
        expr = expr.subs({expr: RandomSymbol(expr.symbol, expr.pspace)})
    else:
        sub = {}
        for arg in expr.args:
            if isinstance(arg, JointRandomSymbol):
                sub[arg] = RandomSymbol(arg.symbol, arg.pspace)
        expr = expr.subs(sub)

    def fn_subs(*args):
        return expr.subs(dict(zip(rvs, args)))

    def given_fn_subs(*args):
        if condition is not None:
            return condition.subs(dict(zip(rvs, args)))
        return False

    if library in ('pymc', 'pymc3'):
        # Currently unable to lambdify in pymc
        # TODO : Remove when lambdify accepts 'pymc' as module
        fn = lambdify(rvs, expr, **kwargs)
    else:
        fn = lambdify(rvs, expr, modules=library, **kwargs)


    if condition is not None:
        given_fn = lambdify(rvs, condition, **kwargs)

    def return_generator_infinite():
        count = 0
        _size = (1,)+((size,) if isinstance(size, int) else size)
        while count < numsamples:
            d = ps.sample(size=_size, library=library, seed=seed)  # a dictionary that maps RVs to values
            args = [d[rv][0] for rv in rvs]

            if condition is not None:  # Check that these values satisfy the condition
                # TODO: Replace the try-except block with only given_fn(*args)
                # once lambdify works with unevaluated SymPy objects.
                try:
                    gd = given_fn(*args)
                except (NameError, TypeError):
                    gd = given_fn_subs(*args)
                if gd != True and gd != False:
                    raise ValueError(
                        "Conditions must not contain free symbols")
                if not gd:  # If the values don't satisfy then try again
                    continue

            yield fn(*args)
            count += 1

    def return_generator_finite():
        faulty = True
        while faulty:
            d = ps.sample(size=(numsamples,) + ((size,) if isinstance(size, int) else size),
                          library=library, seed=seed) # a dictionary that maps RVs to values

            faulty = False
            count = 0
            while count < numsamples and not faulty:
                args = [d[rv][count] for rv in rvs]
                if condition is not None:  # Check that these values satisfy the condition
                    # TODO: Replace the try-except block with only given_fn(*args)
                    # once lambdify works with unevaluated SymPy objects.
                    try:
                        gd = given_fn(*args)
                    except (NameError, TypeError):
                        gd = given_fn_subs(*args)
                    if gd != True and gd != False:
                        raise ValueError(
                            "Conditions must not contain free symbols")
                    if not gd:  # If the values don't satisfy then try again
                        faulty = True

                count += 1

        count = 0
        while count < numsamples:
            args = [d[rv][count] for rv in rvs]
            # TODO: Replace the try-except block with only fn(*args)
            # once lambdify works with unevaluated SymPy objects.
            try:
                yield fn(*args)
            except (NameError, TypeError):
                yield fn_subs(*args)
            count += 1

    if numsamples is S.Infinity:
        return return_generator_infinite()

    return return_generator_finite()

