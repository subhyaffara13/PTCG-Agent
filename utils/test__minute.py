
def test_Minute():
    assert_offset_equal(Minute(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 1))
    assert_offset_equal(Minute(-1), datetime(2010, 1, 1, 0, 1), datetime(2010, 1, 1))
    assert_offset_equal(2 * Minute(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 2))
    assert_offset_equal(-1 * Minute(), datetime(2010, 1, 1, 0, 1), datetime(2010, 1, 1))

    assert Minute(3) + Minute(2) == Minute(5)
    assert Minute(3) - Minute(2) == Minute()
    assert Minute(5) != Minute()

