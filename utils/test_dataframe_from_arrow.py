
def test_dataframe_from_arrow(using_infer_string):
    # objects with __arrow_c_stream__
    table = pa.table({"a": [1, 2, 3], "b": ["a", "b", "c"]})

    result = pd.DataFrame.from_arrow(table)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"]})
    if not using_infer_string:
        expected["b"] = expected["b"].astype(pd.StringDtype(na_value=np.nan))
    tm.assert_frame_equal(result, expected)

    # not only pyarrow object are supported
    result = pd.DataFrame.from_arrow(ArrowStreamWrapper(table))
    tm.assert_frame_equal(result, expected)

    # objects with __arrow_c_array__
    batch = pa.record_batch([[1, 2, 3], ["a", "b", "c"]], names=["a", "b"])

    result = pd.DataFrame.from_arrow(table)
    tm.assert_frame_equal(result, expected)

    result = pd.DataFrame.from_arrow(ArrowArrayWrapper(batch))
    tm.assert_frame_equal(result, expected)

    # only accept actual Arrow objects
    with pytest.raises(TypeError, match="Expected an Arrow-compatible tabular object"):
        pd.DataFrame.from_arrow({"a": [1, 2, 3], "b": ["a", "b", "c"]})


def test_dataframe_from_arrow():
    # objects with __arrow_c_stream__
    arr = pa.chunked_array([[1, 2, 3], [4, 5]])

    result = pd.Series.from_arrow(arr)
    expected = pd.Series([1, 2, 3, 4, 5])
    tm.assert_series_equal(result, expected)

    # not only pyarrow object are supported
    result = pd.Series.from_arrow(ArrowStreamWrapper(arr))
    tm.assert_series_equal(result, expected)

    # table works as well, but will be seen as a StructArray
    table = pa.table({"a": [1, 2, 3], "b": ["a", "b", "c"]})

    result = pd.Series.from_arrow(table)
    expected = pd.Series([{"a": 1, "b": "a"}, {"a": 2, "b": "b"}, {"a": 3, "b": "c"}])
    tm.assert_series_equal(result, expected)

    # objects with __arrow_c_array__
    arr = pa.array([1, 2, 3])

    expected = pd.Series([1, 2, 3])
    result = pd.Series.from_arrow(arr)
    tm.assert_series_equal(result, expected)

    result = pd.Series.from_arrow(ArrowArrayWrapper(arr))
    tm.assert_series_equal(result, expected)

    # only accept actual Arrow objects
    with pytest.raises(
        TypeError, match="Expected an Arrow-compatible array-like object"
    ):
        pd.Series.from_arrow([1, 2, 3])

