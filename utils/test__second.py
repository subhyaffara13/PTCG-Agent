
def test_Second():
    assert_offset_equal(Second(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 0, 1))
    assert_offset_equal(Second(-1), datetime(2010, 1, 1, 0, 0, 1), datetime(2010, 1, 1))
    assert_offset_equal(
        2 * Second(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 0, 2)
    )
    assert_offset_equal(
        -1 * Second(), datetime(2010, 1, 1, 0, 0, 1), datetime(2010, 1, 1)
    )

    assert Second(3) + Second(2) == Second(5)
    assert Second(3) - Second(2) == Second()

