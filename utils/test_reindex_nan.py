
def test_reindex_nan():
    ts = Series([2, 3, 5, 7], index=[1, 4, np.nan, 8])

    i, j = [np.nan, 1, np.nan, 8, 4, np.nan], [2, 0, 2, 3, 1, 2]
    tm.assert_series_equal(ts.reindex(i), ts.iloc[j])

    ts.index = ts.index.astype("object")

    # reindex coerces index.dtype to float, loc/iloc doesn't
    tm.assert_series_equal(ts.reindex(i), ts.iloc[j], check_index_type=False)

