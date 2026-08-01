
def test_R17():
    k = symbols('k', integer=True, positive=True)
    assert abs(float(Sum(1/k**2 + 1/k**3, (k, 1, oo)))
               - 2.8469909700078206) < 1e-15

