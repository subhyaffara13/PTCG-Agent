
def test_nat_vector_field_access():
    idx = DatetimeIndex(["1/1/2000", None, None, "1/4/2000"])

    for field in DatetimeArray._field_ops:
        # weekday is a property of DTI, but a method
        # on NaT/Timestamp for compat with datetime
        if field == "weekday":
            continue

        result = getattr(idx, field)
        expected = Index([getattr(x, field) for x in idx])
        tm.assert_index_equal(result, expected)

    ser = Series(idx)

    for field in DatetimeArray._field_ops:
        # weekday is a property of DTI, but a method
        # on NaT/Timestamp for compat with datetime
        if field == "weekday":
            continue

        result = getattr(ser.dt, field)
        expected = [getattr(x, field) for x in idx]
        tm.assert_series_equal(result, Series(expected))

    for field in DatetimeArray._bool_ops:
        result = getattr(ser.dt, field)
        expected = [getattr(x, field) for x in idx]
        tm.assert_series_equal(result, Series(expected))

