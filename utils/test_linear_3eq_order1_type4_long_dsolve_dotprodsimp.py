
def test_linear_3eq_order1_type4_long_dsolve_dotprodsimp():
    eq, sol = _linear_3eq_order1_type4_long()

    # XXX: Only works with dotprodsimp see
    # test_linear_3eq_order1_type4_long_dsolve_slow_xfail which is too slow
    with dotprodsimp(True):
        dsolve_sol = dsolve(eq)

    dsolve_sol1 = [_simpsol(sol) for sol in dsolve_sol]
    assert dsolve_sol1 == sol

