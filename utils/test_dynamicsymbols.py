
def test_dynamicsymbols():
    #Tests to check the assumptions applied to dynamicsymbols
    f1 = dynamicsymbols('f1')
    f2 = dynamicsymbols('f2', real=True)
    f3 = dynamicsymbols('f3', positive=True)
    f4, f5 = dynamicsymbols('f4,f5', commutative=False)
    f6 = dynamicsymbols('f6', integer=True)
    assert f1.is_real is None
    assert f2.is_real
    assert f3.is_positive
    assert f4*f5 != f5*f4
    assert f6.is_integer

