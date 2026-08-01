
def _lp_matrices(objective, constraints):
    """return A, B, C, D, r, x+X, X for maximizing
    objective = Cx - D with constraints Ax <= B, introducing
    introducing auxilliary variables, X, as necessary to make
    replacements of symbols as given in r, {xi: expression with Xj},
    so all variables in x+X will take on nonnegative values.

    Every univariate condition creates a semi-infinite
    condition, e.g. a single ``x <= 3`` creates the
    interval ``[-oo, 3]`` while ``x <= 3`` and ``x >= 2``
    create an interval ``[2, 3]``. Variables not in a univariate
    expression will take on nonnegative values.
    """

    # sympify input and collect free symbols
    F = sympify(objective)
    np = [sympify(i) for i in constraints]
    syms = set.union(*[i.free_symbols for i in [F] + np], set())

    # change Eq(x, y) to x - y <= 0 and y - x <= 0
    for i in range(len(np)):
        if isinstance(np[i], Eq):
            np[i] = np[i].lhs - np[i].rhs <= 0
            np.append(-np[i].lhs <= 0)

    # convert constraints to nonpositive expressions
    _ = _rel_as_nonpos(np, syms)
    if _ is None:
        raise InfeasibleLPError(filldedent("""
            Inconsistent/False constraint"""))
    np, r, aux = _

    # do change of variables
    F = F.xreplace(r)
    np = [i.xreplace(r) for i in np]

    # convert to matrices
    xx = list(ordered(syms)) + aux
    A, B = linear_eq_to_matrix(np, xx)
    C, D = linear_eq_to_matrix([F], xx)
    return A, B, C, D, r, xx, aux

