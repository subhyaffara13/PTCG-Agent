
def test_M8():
    x = Symbol('x')
    z = symbols('z', complex=True)
    assert solveset(exp(2*x) + 2*exp(x) + 1 - z, x, S.Reals) == \
        FiniteSet(log(1 + z - 2*sqrt(z))/2, log(1 + z + 2*sqrt(z))/2)

