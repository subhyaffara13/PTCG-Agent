
def test_M5():
    assert solveset(x**6 - 9*x**4 - 4*x**3 + 27*x**2 - 36*x - 23, x) == FiniteSet(2**(1/3) + sqrt(3), 2**(1/3) - sqrt(3), +sqrt(3) - 1/2**(2/3) + I*sqrt(3)/2**(2/3), +sqrt(3) - 1/2**(2/3) - I*sqrt(3)/2**(2/3), -sqrt(3) - 1/2**(2/3) + I*sqrt(3)/2**(2/3), -sqrt(3) - 1/2**(2/3) - I*sqrt(3)/2**(2/3))

