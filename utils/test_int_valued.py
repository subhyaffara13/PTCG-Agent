
def test_int_valued():
    x = Symbol('x')
    assert int_valued(x) == False
    assert int_valued(S.Half) == False
    assert int_valued(S.One) == True
    assert int_valued(Float(1)) == True
    assert int_valued(Float(1.1)) == False
    assert int_valued(pi) == False

