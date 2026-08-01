
def test_no_sol():
    assert solveset(1 - oo*x) is S.EmptySet
    assert solveset(oo*x, x) is S.EmptySet
    assert solveset(oo*x - oo, x) is S.EmptySet
    assert solveset_real(4, x) is S.EmptySet
    assert solveset_real(exp(x), x) is S.EmptySet
    assert solveset_real(x**2 + 1, x) is S.EmptySet
    assert solveset_real(-3*a/sqrt(x), x) is S.EmptySet
    assert solveset_real(1/x, x) is S.EmptySet
    assert solveset_real(-(1 + x)/(2 + x)**2 + 1/(2 + x), x
        ) is S.EmptySet

