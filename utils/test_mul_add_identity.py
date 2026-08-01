
def test_mul_add_identity():
    m = Mul(1, 2)
    assert isinstance(m, Rational) and m.p == 2 and m.q == 1
    m = Mul(1, 2, evaluate=False)
    assert isinstance(m, Mul) and m.args == (1, 2)
    m = Mul(0, 1)
    assert m is S.Zero
    m = Mul(0, 1, evaluate=False)
    assert isinstance(m, Mul) and m.args == (0, 1)
    m = Add(0, 1)
    assert m is S.One
    m = Add(0, 1, evaluate=False)
    assert isinstance(m, Add) and m.args == (0, 1)

