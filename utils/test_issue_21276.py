
def test_issue_21276():
    eq = (2*x*(y - z) - y*erf(y - z) - y + z*erf(y - z) + z)**2
    assert solveset(eq.expand(), y) == FiniteSet(z, z + erfinv(2*x - 1))

