
def test_isin_arrow_string_array(dtype):
    pa = pytest.importorskip("pyarrow")
    s = pd.Series(["a", "b", None], dtype=dtype)

    result = s.isin(pd.array(["a", "c"], dtype=pd.ArrowDtype(pa.string())))
    expected = pd.Series([True, False, False])
    tm.assert_series_equal(result, expected)

    result = s.isin(pd.array(["a", None], dtype=pd.ArrowDtype(pa.string())))
    expected = pd.Series([True, False, True])
    tm.assert_series_equal(result, expected)

