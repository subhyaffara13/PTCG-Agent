
def ode_sol_simplicity(sol, func, trysolving=True):
    r"""
    Returns an extended integer representing how simple a solution to an ODE
    is.

    The following things are considered, in order from most simple to least:

    - ``sol`` is solved for ``func``.
    - ``sol`` is not solved for ``func``, but can be if passed to solve (e.g.,
      a solution returned by ``dsolve(ode, func, simplify=False``).
    - If ``sol`` is not solved for ``func``, then base the result on the
      length of ``sol``, as computed by ``len(str(sol))``.
    - If ``sol`` has any unevaluated :py:class:`~sympy.integrals.integrals.Integral`\s,
      this will automatically be considered less simple than any of the above.

    This function returns an integer such that if solution A is simpler than
    solution B by above metric, then ``ode_sol_simplicity(sola, func) <
    ode_sol_simplicity(solb, func)``.

    Currently, the following are the numbers returned, but if the heuristic is
    ever improved, this may change.  Only the ordering is guaranteed.

    +----------------------------------------------+-------------------+
    | Simplicity                                   | Return            |
    +==============================================+===================+
    | ``sol`` solved for ``func``                  | ``-2``            |
    +----------------------------------------------+-------------------+
    | ``sol`` not solved for ``func`` but can be   | ``-1``            |
    +----------------------------------------------+-------------------+
    | ``sol`` is not solved nor solvable for       | ``len(str(sol))`` |
    | ``func``                                     |                   |
    +----------------------------------------------+-------------------+
    | ``sol`` contains an                          | ``oo``            |
    | :obj:`~sympy.integrals.integrals.Integral`   |                   |
    +----------------------------------------------+-------------------+

    ``oo`` here means the SymPy infinity, which should compare greater than
    any integer.

    If you already know :py:meth:`~sympy.solvers.solvers.solve` cannot solve
    ``sol``, you can use ``trysolving=False`` to skip that step, which is the
    only potentially slow step.  For example,
    :py:meth:`~sympy.solvers.ode.dsolve` with the ``simplify=False`` flag
    should do this.

    If ``sol`` is a list of solutions, if the worst solution in the list
    returns ``oo`` it returns that, otherwise it returns ``len(str(sol))``,
    that is, the length of the string representation of the whole list.

    Examples
    ========

    This function is designed to be passed to ``min`` as the key argument,
    such as ``min(listofsolutions, key=lambda i: ode_sol_simplicity(i,
    f(x)))``.

    >>> from sympy import symbols, Function, Eq, tan, Integral
    >>> from sympy.solvers.ode.ode import ode_sol_simplicity
    >>> x, C1, C2 = symbols('x, C1, C2')
    >>> f = Function('f')

    >>> ode_sol_simplicity(Eq(f(x), C1*x**2), f(x))
    -2
    >>> ode_sol_simplicity(Eq(x**2 + f(x), C1), f(x))
    -1
    >>> ode_sol_simplicity(Eq(f(x), C1*Integral(2*x, x)), f(x))
    oo
    >>> eq1 = Eq(f(x)/tan(f(x)/(2*x)), C1)
    >>> eq2 = Eq(f(x)/tan(f(x)/(2*x) + f(x)), C2)
    >>> [ode_sol_simplicity(eq, f(x)) for eq in [eq1, eq2]]
    [28, 35]
    >>> min([eq1, eq2], key=lambda i: ode_sol_simplicity(i, f(x)))
    Eq(f(x)/tan(f(x)/(2*x)), C1)

    """
    # TODO: if two solutions are solved for f(x), we still want to be
    # able to get the simpler of the two

    # See the docstring for the coercion rules.  We check easier (faster)
    # things here first, to save time.

    if iterable(sol):
        # See if there are Integrals
        for i in sol:
            if ode_sol_simplicity(i, func, trysolving=trysolving) == oo:
                return oo

        return len(str(sol))

    if sol.has(Integral):
        return oo

    # Next, try to solve for func.  This code will change slightly when CRootOf
    # is implemented in solve().  Probably a CRootOf solution should fall
    # somewhere between a normal solution and an unsolvable expression.

    # First, see if they are already solved
    if sol.lhs == func and not sol.rhs.has(func) or \
            sol.rhs == func and not sol.lhs.has(func):
        return -2
    # We are not so lucky, try solving manually
    if trysolving:
        try:
            sols = solve(sol, func)
            if not sols:
                raise NotImplementedError
        except NotImplementedError:
            pass
        else:
            return -1

    # Finally, a naive computation based on the length of the string version
    # of the expression.  This may favor combined fractions because they
    # will not have duplicate denominators, and may slightly favor expressions
    # with fewer additions and subtractions, as those are separated by spaces
    # by the printer.

    # Additional ideas for simplicity heuristics are welcome, like maybe
    # checking if a equation has a larger domain, or if constantsimp has
    # introduced arbitrary constants numbered higher than the order of a
    # given ODE that sol is a solution of.
    return len(str(sol))

