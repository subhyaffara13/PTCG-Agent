
def test_invert_Integer():
    assert ~Integer(0b01010101) == Integer(-0b01010110)
    assert ~Integer(0b01010101) == Integer(~0b01010101)
    assert ~(~Integer(0b01010101)) == Integer(0b01010101)

