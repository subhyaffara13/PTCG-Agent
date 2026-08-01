
def test_euler_polynomial_rewrite():
    m = Symbol('m')
    A = euler(m, x).rewrite('Sum')
    assert A.subs({m:3, x:5}).doit() == euler(3, 5)

