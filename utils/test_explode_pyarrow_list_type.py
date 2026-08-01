
def test_explode_pyarrow_list_type(ignore_index, list_type):
    # GH 53602, 61091
    pa = pytest.importorskip("pyarrow")

    data = [
        [None, None],
        [1],
        [],
        [2, 3],
        None,
    ]
    ser = pd.Series(data, dtype=pd.ArrowDtype(getattr(pa, list_type)(pa.int64())))
    result = ser.explode(ignore_index=ignore_index)
    expected = pd.Series(
        data=[None, None, 1, None, 2, 3, None],
        index=None if ignore_index else [0, 0, 1, 2, 3, 3, 4],
        dtype=pd.ArrowDtype(pa.int64()),
    )
    tm.assert_series_equal(result, expected)

