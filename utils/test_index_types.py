
def test_index_types(temp_h5_path):
    values = np.random.default_rng(2).standard_normal(2)

    func = lambda lhs, rhs: tm.assert_series_equal(lhs, rhs, check_index_type=True)

    ser = Series(values, [0, "y"])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, [datetime.datetime.today(), 0])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, ["y", 0])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, [datetime.date.today(), "a"])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, [0, "y"])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, [datetime.datetime.today(), 0])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, ["y", 0])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, [datetime.date.today(), "a"])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, [1.23, "b"])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, [1, 1.53])
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser = Series(values, [1, 5])
    _check_roundtrip(ser, func, path=temp_h5_path)

    dti = DatetimeIndex(["2012-01-01", "2012-01-02"], dtype="M8[ns]")
    ser = Series(values, index=dti)
    _check_roundtrip(ser, func, path=temp_h5_path)

    ser.index = ser.index.as_unit("s")
    _check_roundtrip(ser, func, path=temp_h5_path)

