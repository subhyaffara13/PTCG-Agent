
def _solve_variation_of_parameters(eq, func, roots, homogen_sol, order, match_obj, simplify_flag=True):
    r"""
    Helper function for the method of variation of parameters and nonhomogeneous euler eq.

    See the
    :py:meth:`~sympy.solvers.ode.single.NthLinearConstantCoeffVariationOfParameters`
    docstring for more information on this method.

    The parameter are ``match_obj`` should be a dictionary that has the following
    keys:

    ``list``
    A list of solutions to the homogeneous equation.

    ``sol``
    The general solution.

    """
    f = func.func
    x = func.args[0]
    r = match_obj
    psol = 0
    wr = wronskian(roots, x)

    if simplify_flag:
        wr = simplify(wr)  # We need much better simplification for
                        # some ODEs. See issue 4662, for example.
        # To reduce commonly occurring sin(x)**2 + cos(x)**2 to 1
        wr = trigsimp(wr, deep=True, recursive=True)
    if not wr:
        # The wronskian will be 0 iff the solutions are not linearly
        # independent.
        raise NotImplementedError("Cannot find " + str(order) +
        " solutions to the homogeneous equation necessary to apply " +
        "variation of parameters to " + str(eq) + " (Wronskian == 0)")
    if len(roots) != order:
        raise NotImplementedError("Cannot find " + str(order) +
        " solutions to the homogeneous equation necessary to apply " +
        "variation of parameters to " +
        str(eq) + " (number of terms != order)")
    negoneterm = S.NegativeOne**(order)
    for i in roots:
        psol += negoneterm*Integral(wronskian([sol for sol in roots if sol != i], x)*r[-1]/wr, x)*i/r[order]
        negoneterm *= -1

    if simplify_flag:
        psol = simplify(psol)
        psol = trigsimp(psol, deep=True)
    return Eq(f(x), homogen_sol.rhs + psol)

