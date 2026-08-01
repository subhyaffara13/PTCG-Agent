
def test_deriv_noncommutative():
    A = Symbol("A", commutative=False)
    f = Function("f")
    assert A*f(x)*A == f(x)*A**2
    assert A*f(x).diff(x)*A == f(x).diff(x) * A**2

