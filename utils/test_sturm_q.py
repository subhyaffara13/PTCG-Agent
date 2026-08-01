
def test_sturm_q():
    x = Symbol('x')

    p = x**3 - 7*x + 7
    q = 3*x**2 - 7
    assert sturm_q(p, q, x) == sturm(p)
    assert sturm_q(-p, -q, x) != sturm(-p)

