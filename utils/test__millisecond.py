
def test_Millisecond():
    assert_offset_equal(
        Milli(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 0, 0, 1000)
    )
    assert_offset_equal(
        Milli(-1), datetime(2010, 1, 1, 0, 0, 0, 1000), datetime(2010, 1, 1)
    )
    assert_offset_equal(
        Milli(2), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 0, 0, 2000)
    )
    assert_offset_equal(
        2 * Milli(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 0, 0, 2000)
    )
    assert_offset_equal(
        -1 * Milli(), datetime(2010, 1, 1, 0, 0, 0, 1000), datetime(2010, 1, 1)
    )

    assert Milli(3) + Milli(2) == Milli(5)
    assert Milli(3) - Milli(2) == Milli()

