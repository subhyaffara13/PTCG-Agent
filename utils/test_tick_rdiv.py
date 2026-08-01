
def test_tick_rdiv(cls):
    off = cls(10)
    delta = off._as_pd_timedelta
    td64 = delta.to_timedelta64()
    instance__type = ".".join([cls.__module__, cls.__name__])
    msg = (
        f"unsupported operand type\\(s\\) for \\/: 'int'|'float' and '{instance__type}'"
    )

    with pytest.raises(TypeError, match=msg):
        2 / off
    with pytest.raises(TypeError, match=msg):
        2.0 / off

    assert (td64 * 2.5) / off == 2.5

    if cls is not Nano:
        # skip pytimedelta for Nano since it gets dropped
        assert (delta.to_pytimedelta() * 2) / off == 2

    result = np.array([2 * td64, td64]) / off
    expected = np.array([2.0, 1.0])
    tm.assert_numpy_array_equal(result, expected)

