
def test_Mul_with_zero_infinite():
    zer = Dummy(zero=True)
    inf = Dummy(finite=False)

    e = Mul(zer, inf, evaluate=False)
    assert e.is_extended_positive is None
    assert e.is_hermitian is None

    e = Mul(inf, zer, evaluate=False)
    assert e.is_extended_positive is None
    assert e.is_hermitian is None

