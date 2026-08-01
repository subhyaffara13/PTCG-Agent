
def test_Microsecond():
    assert_offset_equal(Micro(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 0, 0, 1))
    assert_offset_equal(
        Micro(-1), datetime(2010, 1, 1, 0, 0, 0, 1), datetime(2010, 1, 1)
    )

    assert_offset_equal(
        2 * Micro(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 0, 0, 2)
    )
    assert_offset_equal(
        -1 * Micro(), datetime(2010, 1, 1, 0, 0, 0, 1), datetime(2010, 1, 1)
    )

    assert Micro(3) + Micro(2) == Micro(5)
    assert Micro(3) - Micro(2) == Micro()

