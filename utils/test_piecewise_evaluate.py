
def test_piecewise_evaluate():
    assert Piecewise((x, True)) == x
    assert Piecewise((x, True), evaluate=True) == x
    assert Piecewise((1, Eq(1, x))).args == ((1, Eq(x, 1)),)
    assert Piecewise((1, Eq(1, x)), evaluate=False).args == (
        (1, Eq(1, x)),)
    # like the additive and multiplicative identities that
    # cannot be kept in Add/Mul, we also do not keep a single True
    p = Piecewise((x, True), evaluate=False)
    assert p == x

