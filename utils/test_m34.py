
def test_M34():
    z = symbols('z', complex=True)
    assert solveset((1 + I) * z + (2 - I) * conjugate(z) + 3*I, z) == FiniteSet(2 + 3*I)

