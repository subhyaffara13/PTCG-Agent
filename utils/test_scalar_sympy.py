
def test_scalar_sympy():
    assert represent(Integer(1)) == Integer(1)
    assert represent(Float(1.0)) == Float(1.0)
    assert represent(1.0 + I) == 1.0 + I

