
def test_linear_3eq_order1_type4_long_dsolve_slow_xfail():
    eq, sol = _linear_3eq_order1_type4_long()

    dsolve_sol = dsolve(eq)
    dsolve_sol1 = [_simpsol(sol) for sol in dsolve_sol]

    assert dsolve_sol1 == sol

