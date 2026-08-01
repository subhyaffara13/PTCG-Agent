
def test_order_noncommutative():
    A = Symbol('A', commutative=False)
    assert Order(A + A*x, x) == Order(1, x)
    assert (A + A*x)*Order(x) == Order(x)
    assert (A*x)*Order(x) == Order(x**2, x)
    assert expand((1 + Order(x))*A*A*x) == A*A*x + Order(x**2, x)
    assert expand((A*A + Order(x))*x) == A*A*x + Order(x**2, x)
    assert expand((A + Order(x))*A*x) == A*A*x + Order(x**2, x)

