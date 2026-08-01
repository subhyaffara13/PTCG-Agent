
def test_M29():
    x = symbols('x')
    assert solveset(abs(x - 1) - 2, domain=S.Reals) == FiniteSet(-1, 3)

