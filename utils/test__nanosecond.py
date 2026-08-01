
def test_Nanosecond():
    timestamp = Timestamp(datetime(2010, 1, 1))
    assert_offset_equal(Nano(), timestamp, timestamp + np.timedelta64(1, "ns"))
    assert_offset_equal(Nano(-1), timestamp + np.timedelta64(1, "ns"), timestamp)
    assert_offset_equal(2 * Nano(), timestamp, timestamp + np.timedelta64(2, "ns"))
    assert_offset_equal(-1 * Nano(), timestamp + np.timedelta64(1, "ns"), timestamp)

    assert Nano(3) + Nano(2) == Nano(5)
    assert Nano(3) - Nano(2) == Nano()

    # GH9284
    assert Nano(1) + Nano(10) == Nano(11)
    assert Nano(5) + Micro(1) == Nano(1005)
    assert Micro(5) + Nano(1) == Nano(5001)

