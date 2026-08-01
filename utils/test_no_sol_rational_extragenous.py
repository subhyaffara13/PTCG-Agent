
def test_no_sol_rational_extragenous():
    assert solveset_real((x/(x + 1) + 3)**(-2), x) is S.EmptySet
    assert solveset_real((x - 1)/(1 + 1/(x - 1)), x) is S.EmptySet

