from typing import Union

def solve_decomposition(f, symbol, domain):
    """
    Function to solve equations via the principle of "Decomposition
    and Rewriting".

    Examples
    ========
    >>> from sympy import exp, sin, Symbol, pprint, S
    >>> from sympy.solvers.solveset import solve_decomposition as sd
    >>> x = Symbol('x')
    >>> f1 = exp(2*x) - 3*exp(x) + 2
    >>> sd(f1, x, S.Reals)
    {0, log(2)}
    >>> f2 = sin(x)**2 + 2*sin(x) + 1
    >>> pprint(sd(f2, x, S.Reals), use_unicode=False)
              3*pi
    {2*n*pi + ---- | n in Integers}
               2
    >>> f3 = sin(x + 2)
    >>> pprint(sd(f3, x, S.Reals), use_unicode=False)
    {2*n*pi - 2 | n in Integers} U {2*n*pi - 2 + pi | n in Integers}

    """
    from sympy.solvers.decompogen import decompogen
    # decompose the given function
    g_s = decompogen(f, symbol)
    # `y_s` represents the set of values for which the function `g` is to be
    # solved.
    # `solutions` represent the solutions of the equations `g = y_s` or
    # `g = 0` depending on the type of `y_s`.
    # As we are interested in solving the equation: f = 0
    y_s = FiniteSet(0)
    for g in g_s:
        frange = function_range(g, symbol, domain)
        y_s = Intersection(frange, y_s)
        result = S.EmptySet
        if isinstance(y_s, FiniteSet):
            for y in y_s:
                solutions = solveset(Eq(g, y), symbol, domain)
                if not isinstance(solutions, ConditionSet):
                    result += solutions

        else:
            if isinstance(y_s, ImageSet):
                iter_iset = (y_s,)

            elif isinstance(y_s, Union):
                iter_iset = y_s.args

            elif y_s is S.EmptySet:
                # y_s is not in the range of g in g_s, so no solution exists
                #in the given domain
                return S.EmptySet

            for iset in iter_iset:
                new_solutions = solveset(Eq(iset.lamda.expr, g), symbol, domain)
                dummy_var = tuple(iset.lamda.expr.free_symbols)[0]
                (base_set,) = iset.base_sets
                if isinstance(new_solutions, FiniteSet):
                    new_exprs = new_solutions

                elif isinstance(new_solutions, Intersection):
                    if isinstance(new_solutions.args[1], FiniteSet):
                        new_exprs = new_solutions.args[1]

                for new_expr in new_exprs:
                    result += ImageSet(Lambda(dummy_var, new_expr), base_set)

        if result is S.EmptySet:
            return ConditionSet(symbol, Eq(f, 0), domain)

        y_s = result

    return y_s

