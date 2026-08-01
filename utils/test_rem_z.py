
def test_rem_z():
    x = Symbol('x')

    p = x**8 + x**6 - 3*x**4 - 3*x**3 + 8*x**2 + 2*x - 5
    q = 3*x**6 + 5*x**4 - 4*x**2 - 9*x + 21
    assert rem_z(p, -q, x) != prem(p, -q, x)

