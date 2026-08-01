
def test_or_Integer():
    assert Integer(0b01010101) | Integer(0b10101010) == Integer(0b11111111)
    assert Integer(0b01010101) | 0b10101010 == Integer(0b11111111)
    assert 0b01010101 | Integer(0b10101010) == Integer(0b11111111)

    assert Integer(0b01010101) | Integer(0b11011011) == Integer(0b11011111)
    assert Integer(0b01010101) | 0b11011011 == Integer(0b11011111)
    assert 0b01010101 | Integer(0b11011011) == Integer(0b11011111)

    assert -Integer(0b01010101) | Integer(0b11011011) == Integer(-0b01010101 | 0b11011011)
    assert Integer(-0b01010101) | 0b11011011 == Integer(-0b01010101 | 0b11011011)
    assert -0b01010101 | Integer(0b11011011) == Integer(-0b01010101 | 0b11011011)

    assert Integer(0b01010101) | -Integer(0b11011011) == Integer(0b01010101 | -0b11011011)
    assert Integer(0b01010101) | -0b11011011 == Integer(0b01010101 | -0b11011011)
    assert 0b01010101 | Integer(-0b11011011) == Integer(0b01010101 | -0b11011011)

    raises(TypeError, lambda: Integer(2) | 0.0)
    raises(TypeError, lambda: 0.0 | Integer(2))

