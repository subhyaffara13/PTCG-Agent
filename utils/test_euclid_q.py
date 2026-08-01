
def test_euclid_q():
    x = Symbol('x')

    p = x**3 - 7*x + 7
    q = 3*x**2 - 7
    assert euclid_q(p, q, x)[-1] == -sturm(p)[-1]

