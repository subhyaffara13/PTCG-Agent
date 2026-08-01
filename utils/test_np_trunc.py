
def test_np_trunc():
    # This used to test np.fix, which is not a ufunc but is composed of
    # several ufunc calls under the hood with `out` and `where` keywords. But numpy
    # is deprecating that (or at least discussing deprecating) in favor of np.trunc,
    # which _is_ a ufunc without the out keyword usage.
    ser = pd.Series([-1.5, -0.5, 0.5, 1.5])
    result = np.trunc(ser)
    expected = pd.Series([-1.0, -0.0, 0.0, 1.0])
    tm.assert_series_equal(result, expected)

