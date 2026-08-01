
def test_tick_mul_float():
    off = Micro(2)

    # Case where we retain type
    result = off * 1.5
    expected = Micro(3)
    assert result == expected
    assert isinstance(result, Micro)

    # Case where we bump up to the next type
    result = off * 1.25
    expected = Nano(2500)
    assert result == expected
    assert isinstance(result, Nano)

