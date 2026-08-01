
def test_pickle_roundtrip(data):
    # GH 42600
    expected = pd.Series(data)
    expected_sliced = expected.head(2)
    full_pickled = pickle.dumps(expected)
    sliced_pickled = pickle.dumps(expected_sliced)

    assert len(full_pickled) > len(sliced_pickled)

    result = pickle.loads(full_pickled)
    tm.assert_series_equal(result, expected)

    result_sliced = pickle.loads(sliced_pickled)
    tm.assert_series_equal(result_sliced, expected_sliced)


def test_pickle_roundtrip():
    # https://github.com/pandas-dev/pandas/issues/31847
    result = pickle.loads(pickle.dumps(NA))
    assert result is NA


def test_pickle_roundtrip(na_value):
    # GH 42600
    pytest.importorskip("pyarrow")
    dtype = StringDtype("pyarrow", na_value=na_value)
    expected = pd.Series(range(10), dtype=dtype)
    expected_sliced = expected.head(2)
    full_pickled = pickle.dumps(expected)
    sliced_pickled = pickle.dumps(expected_sliced)

    assert len(full_pickled) > len(sliced_pickled)

    result = pickle.loads(full_pickled)
    tm.assert_series_equal(result, expected)

    result_sliced = pickle.loads(sliced_pickled)
    tm.assert_series_equal(result_sliced, expected_sliced)

