
def test_setitem(xp):
    tf = RigidTransform.from_translation(xp.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    single = RigidTransform.from_translation(xp.asarray([1, 1, 1]))
    double = RigidTransform.from_translation(xp.asarray([[2, 2, 2], [3, 3, 3]]))
    triple = RigidTransform.from_translation(xp.asarray([[3, 3, 3],
                                                         [4, 4, 4],
                                                         [5, 5, 5]]))

    # Test indexing with integer index
    tf[0] = single
    xp_assert_close(tf.translation, xp.asarray([[1.0, 1, 1], [4, 5, 6], [7, 8, 9]]))

    # Test indexing with slice
    tf = RigidTransform.from_translation(xp.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    tf[:2] = double
    xp_assert_close(tf.translation, xp.asarray([[2.0, 2, 2], [3, 3, 3], [7, 8, 9]]))

    # Test indexing with ellipsis
    tf = RigidTransform.from_translation(xp.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    tf[...] = triple
    xp_assert_close(tf.translation, xp.asarray([[3.0, 3, 3], [4, 4, 4], [5, 5, 5]]))

    # Test indexing with boolean array
    tf = RigidTransform.from_translation(xp.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    mask = xp.asarray([True, False, True])
    tf[mask] = double
    xp_assert_close(tf.translation, xp.asarray([[2.0, 2, 2], [4, 5, 6], [3, 3, 3]]))


def test_setitem(key, value, expected):
    arr = PeriodArray(np.arange(3), dtype="period[D]")
    expected = PeriodArray(expected, dtype="period[D]")
    arr[key] = value
    tm.assert_period_array_equal(arr, expected)


def test_setitem(datetime_series):
    datetime_series[datetime_series.index[5]] = np.nan
    datetime_series.iloc[[1, 2, 17]] = np.nan
    datetime_series.iloc[6] = np.nan
    assert np.isnan(datetime_series.iloc[6])
    assert np.isnan(datetime_series.iloc[2])
    datetime_series[np.isnan(datetime_series)] = 5
    assert not np.isnan(datetime_series.iloc[2])


def test_setitem(any_numpy_array):
    nparr = any_numpy_array
    arr = NumpyExtensionArray(nparr, copy=True)

    arr[0] = arr[1]
    nparr[0] = nparr[1]

    tm.assert_numpy_array_equal(arr.to_numpy(), nparr)


def test_setitem(multiple_chunks, key, value, expected):
    pa = pytest.importorskip("pyarrow")

    result = pa.array(list("abcde"))
    expected = pa.array(expected)

    if multiple_chunks:
        result = pa.chunked_array([result[:3], result[3:]])
        expected = pa.chunked_array([expected[:3], expected[3:]])

    result = ArrowStringArray(result)
    expected = ArrowStringArray(expected)

    result[key] = value
    tm.assert_equal(result, expected)

