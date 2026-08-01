
def test_where_datetimelike_categorical(tz_naive_fixture):
    # GH#37682
    tz = tz_naive_fixture

    dr = date_range("2001-01-01", periods=3, tz=tz)._with_freq(None)
    lvals = pd.DatetimeIndex([dr[0], dr[1], pd.NaT])
    rvals = pd.Categorical([dr[0], pd.NaT, dr[2]])

    mask = np.array([True, True, False])

    # DatetimeIndex.where
    res = lvals.where(mask, rvals)
    tm.assert_index_equal(res, dr)

    # DatetimeArray.where
    res = lvals._data._where(mask, rvals)
    tm.assert_datetime_array_equal(res, dr._data)

    # Series.where
    res = Series(lvals).where(mask, rvals)
    tm.assert_series_equal(res, Series(dr))

    # DataFrame.where
    res = pd.DataFrame(lvals).where(mask[:, None], pd.DataFrame(rvals))

    tm.assert_frame_equal(res, pd.DataFrame(dr))

