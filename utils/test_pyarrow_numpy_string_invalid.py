
def test_pyarrow_numpy_string_invalid():
    # GH#56008
    pa = pytest.importorskip("pyarrow")
    ser = Series([False, True])
    ser2 = Series(["a", "b"], dtype=StringDtype(na_value=np.nan))
    result = ser == ser2
    expected_eq = Series(False, index=ser.index)
    tm.assert_series_equal(result, expected_eq)

    result = ser != ser2
    expected_ne = Series(True, index=ser.index)
    tm.assert_series_equal(result, expected_ne)

    with pytest.raises(TypeError, match="Invalid comparison"):
        ser > ser2

    # GH#59505
    ser3 = ser2.astype("string[pyarrow]")
    result3_eq = ser3 == ser
    tm.assert_series_equal(result3_eq, expected_eq.astype("bool[pyarrow]"))
    result3_ne = ser3 != ser
    tm.assert_series_equal(result3_ne, expected_ne.astype("bool[pyarrow]"))

    with pytest.raises(TypeError, match="Invalid comparison"):
        ser > ser3

    ser4 = ser2.astype(ArrowDtype(pa.string()))
    result4_eq = ser4 == ser
    tm.assert_series_equal(result4_eq, expected_eq.astype("bool[pyarrow]"))
    result4_ne = ser4 != ser
    tm.assert_series_equal(result4_ne, expected_ne.astype("bool[pyarrow]"))

    with pytest.raises(TypeError, match="Invalid comparison"):
        ser > ser4

