
def test_slice():
    assert aesara_code_(slice(1, 2, 3)) == slice(1, 2, 3)

    def theq_slice(s1, s2):
        for attr in ['start', 'stop', 'step']:
            a1 = getattr(s1, attr)
            a2 = getattr(s2, attr)
            if a1 is None or a2 is None:
                if not (a1 is None or a2 is None):
                    return False
            elif not theq(a1, a2):
                return False
        return True

    dtypes = {x: 'int32', y: 'int32'}
    assert theq_slice(aesara_code_(slice(x, y), dtypes=dtypes), slice(xt, yt))
    assert theq_slice(aesara_code_(slice(1, x, 3), dtypes=dtypes), slice(1, xt, 3))


def test_slice():
    assert theano_code_(slice(1, 2, 3)) == slice(1, 2, 3)

    def theq_slice(s1, s2):
        for attr in ['start', 'stop', 'step']:
            a1 = getattr(s1, attr)
            a2 = getattr(s2, attr)
            if a1 is None or a2 is None:
                if not (a1 is None or a2 is None):
                    return False
            elif not theq(a1, a2):
                return False
        return True

    dtypes = {x: 'int32', y: 'int32'}
    assert theq_slice(theano_code_(slice(x, y), dtypes=dtypes), slice(xt, yt))
    assert theq_slice(theano_code_(slice(1, x, 3), dtypes=dtypes), slice(1, xt, 3))


def test_slice(slice_test_df, slice_test_grouped):
    # Test single slice
    result = slice_test_grouped._positional_selector[0:3:2]
    expected = slice_test_df.iloc[[0, 1, 4, 5]]

    tm.assert_frame_equal(result, expected)


def test_slice(start, stop, step, expected, any_string_dtype):
    ser = Series(["aafootwo", "aabartwo", np.nan, "aabazqux"], dtype=any_string_dtype)
    result = ser.str.slice(start, stop, step)
    expected = Series(expected, dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)


def test_slice(string_series, object_series):
    original = string_series.copy()
    numSlice = string_series[10:20]
    numSliceEnd = string_series[-10:]
    objSlice = object_series[10:20]

    assert string_series.index[9] not in numSlice.index
    assert object_series.index[9] not in objSlice.index

    assert len(numSlice) == len(numSlice.index)
    assert string_series[numSlice.index[0]] == numSlice[numSlice.index[0]]

    assert numSlice.index[1] == string_series.index[11]
    tm.assert_numpy_array_equal(np.array(numSliceEnd), np.array(string_series)[-10:])

    # Test return view.
    sl = string_series[10:20]
    sl[:] = 0

    # Doesn't modify parent (CoW)
    tm.assert_series_equal(string_series, original)


def test_slice(slice_test_df, slice_test_grouped, arg, expected_rows):
    # Test slices     GH #42947

    result = slice_test_grouped.nth[arg]
    equivalent = slice_test_grouped.nth(arg)
    expected = slice_test_df.iloc[expected_rows]

    tm.assert_frame_equal(result, expected)
    tm.assert_frame_equal(equivalent, expected)

