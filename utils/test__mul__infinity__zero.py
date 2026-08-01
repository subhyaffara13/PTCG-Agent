
def test_Mul_Infinity_Zero():
    assert Float(0)*_inf is nan
    assert Float(0)*_ninf is nan
    assert Float(0)*_inf is nan
    assert Float(0)*_ninf is nan
    assert _inf*Float(0) is nan
    assert _ninf*Float(0) is nan
    assert _inf*Float(0) is nan
    assert _ninf*Float(0) is nan

