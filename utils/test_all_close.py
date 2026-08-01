
def test_all_close():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    assert all_close(2, 2) is True
    assert all_close(2, 2.0000) is True
    assert all_close(2, 2.0001) is False
    assert all_close(1/3, 1/3.0001) is False
    assert all_close(1/3, 1/3.0001, 1e-3, 1e-3) is True
    assert all_close(1/3, Rational(1, 3)) is True
    assert all_close(0.1*exp(0.2*x), exp(x/5)/10) is True
    # The expressions should be structurally the same modulo identity:
    assert all_close(1.4142135623730951, sqrt(2)) is False
    assert all_close(1.4142135623730951, sqrt(2).evalf()) is True
    assert all_close(x + 1e-20, x) is True
    # We should be able to match terms of an Add/Mul in any order
    assert all_close(Add(1, 2, evaluate=False), Add(2, 1, evaluate=False))
    # coverage
    assert not all_close(2*x, 3*x)
    assert all_close(2*x, 3*x, 1)
    assert not all_close(2*x, 3*x, 0, 0.5)
    assert all_close(2*x, 3*x, 0, 1)
    assert not all_close(y*x, z*x)
    assert all_close(2*x*exp(1.0*x), 2.0*x*exp(x))
    assert not all_close(2*x*exp(1.0*x), 2.0*x*exp(2.*x))
    assert all_close(x + 2.*y, 1.*x + 2*y)
    assert all_close(x + exp(2.*x)*y, 1.*x + exp(2*x)*y)
    assert not all_close(x + exp(2.*x)*y, 1.*x + 2*exp(2*x)*y)
    assert not all_close(x + exp(2.*x)*y, 1.*x + exp(3*x)*y)
    assert not all_close(x + 2.*y, 1.*x + 3*y)

