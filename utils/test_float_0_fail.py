
def test_float_0_fail():
    assert Float(0.0)*x == Float(0.0)
    assert (x + Float(0.0)).is_Add

