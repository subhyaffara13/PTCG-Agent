from typing import Tuple

def dsolve_system(eqs, funcs=None, t=None, ics=None, doit=False, simplify=True):
    r"""
    Solves any(supported) system of Ordinary Differential Equations

    Explanation
    ===========

    This function takes a system of ODEs as an input, determines if the
    it is solvable by this function, and returns the solution if found any.

    This function can handle:
    1. Linear, First Order, Constant coefficient homogeneous system of ODEs
    2. Linear, First Order, Constant coefficient non-homogeneous system of ODEs
    3. Linear, First Order, non-constant coefficient homogeneous system of ODEs
    4. Linear, First Order, non-constant coefficient non-homogeneous system of ODEs
    5. Any implicit system which can be divided into system of ODEs which is of the above 4 forms
    6. Any higher order linear system of ODEs that can be reduced to one of the 5 forms of systems described above.

    The types of systems described above are not limited by the number of equations, i.e. this
    function can solve the above types irrespective of the number of equations in the system passed.
    But, the bigger the system, the more time it will take to solve the system.

    This function returns a list of solutions. Each solution is a list of equations where LHS is
    the dependent variable and RHS is an expression in terms of the independent variable.

    Among the non constant coefficient types, not all the systems are solvable by this function. Only
    those which have either a coefficient matrix with a commutative antiderivative or those systems which
    may be divided further so that the divided systems may have coefficient matrix with commutative antiderivative.

    Parameters
    ==========

    eqs : List
        system of ODEs to be solved
    funcs : List or None
        List of dependent variables that make up the system of ODEs
    t : Symbol or None
        Independent variable in the system of ODEs
    ics : Dict or None
        Set of initial boundary/conditions for the system of ODEs
    doit : Boolean
        Evaluate the solutions if True. Default value is True. Can be
        set to false if the integral evaluation takes too much time and/or
        is not required.
    simplify: Boolean
        Simplify the solutions for the systems. Default value is True.
        Can be set to false if simplification takes too much time and/or
        is not required.

    Examples
    ========

    >>> from sympy import symbols, Eq, Function
    >>> from sympy.solvers.ode.systems import dsolve_system
    >>> f, g = symbols("f g", cls=Function)
    >>> x = symbols("x")

    >>> eqs = [Eq(f(x).diff(x), g(x)), Eq(g(x).diff(x), f(x))]
    >>> dsolve_system(eqs)
    [[Eq(f(x), -C1*exp(-x) + C2*exp(x)), Eq(g(x), C1*exp(-x) + C2*exp(x))]]

    You can also pass the initial conditions for the system of ODEs:

    >>> dsolve_system(eqs, ics={f(0): 1, g(0): 0})
    [[Eq(f(x), exp(x)/2 + exp(-x)/2), Eq(g(x), exp(x)/2 - exp(-x)/2)]]

    Optionally, you can pass the dependent variables and the independent
    variable for which the system is to be solved:

    >>> funcs = [f(x), g(x)]
    >>> dsolve_system(eqs, funcs=funcs, t=x)
    [[Eq(f(x), -C1*exp(-x) + C2*exp(x)), Eq(g(x), C1*exp(-x) + C2*exp(x))]]

    Lets look at an implicit system of ODEs:

    >>> eqs = [Eq(f(x).diff(x)**2, g(x)**2), Eq(g(x).diff(x), g(x))]
    >>> dsolve_system(eqs)
    [[Eq(f(x), C1 - C2*exp(x)), Eq(g(x), C2*exp(x))], [Eq(f(x), C1 + C2*exp(x)), Eq(g(x), C2*exp(x))]]

    Returns
    =======

    List of List of Equations

    Raises
    ======

    NotImplementedError
        When the system of ODEs is not solvable by this function.
    ValueError
        When the parameters passed are not in the required form.

    """
    from sympy.solvers.ode.ode import solve_ics, _extract_funcs, constant_renumber

    if not iterable(eqs):
        raise ValueError(filldedent('''
            List of equations should be passed. The input is not valid.
        '''))

    eqs = _preprocess_eqs(eqs)

    if funcs is not None and not isinstance(funcs, list):
        raise ValueError(filldedent('''
            Input to the funcs should be a list of functions.
        '''))

    if funcs is None:
        funcs = _extract_funcs(eqs)

    if any(len(func.args) != 1 for func in funcs):
        raise ValueError(filldedent('''
            dsolve_system can solve a system of ODEs with only one independent
            variable.
        '''))

    if len(eqs) != len(funcs):
        raise ValueError(filldedent('''
            Number of equations and number of functions do not match
        '''))

    if t is not None and not isinstance(t, Symbol):
        raise ValueError(filldedent('''
            The independent variable must be of type Symbol
        '''))

    if t is None:
        t = list(list(eqs[0].atoms(Derivative))[0].atoms(Symbol))[0]

    sols = []
    canon_eqs = canonical_odes(eqs, funcs, t)

    for canon_eq in canon_eqs:
        try:
            sol = _strong_component_solver(canon_eq, funcs, t)
        except NotImplementedError:
            sol = None

        if sol is None:
            sol = _component_solver(canon_eq, funcs, t)

        sols.append(sol)

    if sols:
        final_sols = []
        variables = Tuple(*eqs).free_symbols

        for sol in sols:

            sol = _select_equations(sol, funcs)
            sol = constant_renumber(sol, variables=variables)

            if ics:
                constants = Tuple(*sol).free_symbols - variables
                solved_constants = solve_ics(sol, funcs, constants, ics)
                sol = [s.subs(solved_constants) for s in sol]

            if simplify:
                constants = Tuple(*sol).free_symbols - variables
                sol = simpsol(sol, [t], constants, doit=doit)

            final_sols.append(sol)

        sols = final_sols

    return sols

