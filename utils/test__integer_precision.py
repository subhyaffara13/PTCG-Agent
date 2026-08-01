
def test_Integer_precision():
    # Make sure Integer inputs for keyword args work
    assert Float('1.0', dps=Integer(15))._prec == 53
    assert Float('1.0', precision=Integer(15))._prec == 15
    assert type(Float('1.0', precision=Integer(15))._prec) == int
    assert sympify(srepr(Float('1.0', precision=15))) == Float('1.0', precision=15)

