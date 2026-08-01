
def test_rshift_Integer():
    assert Integer(0) >> Integer(2) == Integer(0)
    assert Integer(0) >> 2 == Integer(0)
    assert 0 >> Integer(2) == Integer(0)

    assert Integer(0b11) >> Integer(0) == Integer(0b11)
    assert Integer(0b11) >> 0 == Integer(0b11)
    assert 0b11 >> Integer(0) == Integer(0b11)

    assert Integer(0b11) >> Integer(2) == Integer(0)
    assert Integer(0b11) >> 2 == Integer(0)
    assert 0b11 >> Integer(2) == Integer(0)

    assert Integer(-0b11) >> Integer(2) == Integer(-1)
    assert Integer(-0b11) >> 2 == Integer(-1)
    assert -0b11 >> Integer(2) == Integer(-1)

    assert Integer(0b1100) >> Integer(2) == Integer(0b1100 >> 2)
    assert Integer(0b1100) >> 2 == Integer(0b1100 >> 2)
    assert 0b1100 >> Integer(2) == Integer(0b1100 >> 2)

    assert Integer(-0b1100) >> Integer(2) == Integer(-0b1100 >> 2)
    assert Integer(-0b1100) >> 2 == Integer(-0b1100 >> 2)
    assert -0b1100 >> Integer(2) == Integer(-0b1100 >> 2)

    raises(TypeError, lambda: Integer(0b10) >> 0.0)
    raises(TypeError, lambda: 0.0 >> Integer(2))
    raises(ValueError, lambda: Integer(1) >> Integer(-1))

