
def merge_solution(var, var_t, solution):
    """
    This is used to construct the full solution from the solutions of sub
    equations.

    Explanation
    ===========

    For example when solving the equation `(x - y)(x^2 + y^2 - z^2) = 0`,
    solutions for each of the equations `x - y = 0` and `x^2 + y^2 - z^2` are
    found independently. Solutions for `x - y = 0` are `(x, y) = (t, t)`. But
    we should introduce a value for z when we output the solution for the
    original equation. This function converts `(t, t)` into `(t, t, n_{1})`
    where `n_{1}` is an integer parameter.
    """
    sol = []

    if None in solution:
        return ()

    solution = iter(solution)
    params = numbered_symbols("n", integer=True, start=1)
    for v in var:
        if v in var_t:
            sol.append(next(solution))
        else:
            sol.append(next(params))

    for val, symb in zip(sol, var):
        if check_assumptions(val, **symb.assumptions0) is False:
            return ()

    return tuple(sol)

