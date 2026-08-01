
def test_function_complex():
    x = Symbol('x', complex=True)
    xzf = Symbol('x', complex=True, zero=False)
    assert f(x).is_commutative is True
    assert sin(x).is_commutative is True
    assert exp(x).is_commutative is True
    assert log(x).is_commutative is True
    assert f(x).is_complex is None
    assert sin(x).is_complex is True
    assert exp(x).is_complex is True
    assert log(x).is_complex is None
    assert log(xzf).is_complex is True

