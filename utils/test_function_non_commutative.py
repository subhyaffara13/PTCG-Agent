
def test_function_non_commutative():
    x = Symbol('x', commutative=False)
    assert f(x).is_commutative is False
    assert sin(x).is_commutative is False
    assert exp(x).is_commutative is False
    assert log(x).is_commutative is False
    assert f(x).is_complex is False
    assert sin(x).is_complex is False
    assert exp(x).is_complex is False
    assert log(x).is_complex is False

