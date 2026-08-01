
def test_Mult1(offset_box, offset1):
    dt = Timestamp(2008, 1, 2)
    assert dt + 10 * offset1 == dt + offset_box(10)
    assert dt + 5 * offset1 == dt + offset_box(5)

