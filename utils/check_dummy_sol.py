
def check_dummy_sol(eq, solse, dummy_sym):
    """
    Helper function to check if actual solution
    matches expected solution if actual solution
    contains dummy symbols.
    """
    if isinstance(eq, Eq):
        eq = eq.lhs - eq.rhs
    _, funcs = match_riccati(eq, f, x)

    sols = solve_riccati(f(x), x, *funcs)
    C1 = Dummy('C1')
    sols = [sol.subs(C1, dummy_sym) for sol in sols]

    assert all(x[0] for x in checkodesol(eq, sols))
    assert all(s1.dummy_eq(s2, dummy_sym) for s1, s2 in zip(sols, solse))

