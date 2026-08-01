
def test_purestr():
    assert purestr(Symbol('x')) == "Symbol('x')"
    assert purestr(Basic(S(1), S(2))) == "Basic(Integer(1), Integer(2))"
    assert purestr(Float(2)) == "Float('2.0', precision=53)"

    assert purestr(Symbol('x'), with_args=True) == ("Symbol('x')", ())
    assert purestr(Basic(S(1), S(2)), with_args=True) == \
            ('Basic(Integer(1), Integer(2))', ('Integer(1)', 'Integer(2)'))
    assert purestr(Float(2), with_args=True) == \
        ("Float('2.0', precision=53)", ())

