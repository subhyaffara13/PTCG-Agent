
def test_Mul_does_not_distribute_infinity():
    a, b = symbols('a b')
    assert ((1 + I)*oo).is_Mul
    assert ((a + b)*(-oo)).is_Mul
    assert ((a + 1)*zoo).is_Mul
    assert ((1 + I)*oo).is_finite is False
    z = (1 + I)*oo
    assert ((1 - I)*z).expand() is oo

