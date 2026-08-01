
def test_symbol_noncommutative():
    x = Symbol('x', commutative=True)
    assert x.is_complex is None

    x = Symbol('x', commutative=False)
    assert x.is_integer is False
    assert x.is_rational is False
    assert x.is_algebraic is False
    assert x.is_irrational is False
    assert x.is_real is False
    assert x.is_complex is False

