
def test_select_iterator_complete_8014_full_range(temp_hdfstore):
    # GH 8014
    chunksize = 1e4
    expected = DataFrame(
        np.random.default_rng(2).standard_normal((100064, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=100064, freq="s", unit="ns"),
    )
    temp_hdfstore.append("df", expected)

    beg_dt = expected.index[0]
    end_dt = expected.index[-1]

    # select w/iterator and no where clause works
    results = list(temp_hdfstore.select("df", chunksize=chunksize))
    result = concat(results)
    tm.assert_frame_equal(expected, result)

    # select w/iterator and where clause, single term, begin of range
    where = f"index >= '{beg_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))
    result = concat(results)
    tm.assert_frame_equal(expected, result)

    # select w/iterator and where clause, single term, end of range
    where = f"index <= '{end_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))
    result = concat(results)
    tm.assert_frame_equal(expected, result)

    # select w/iterator and where clause, inclusive range
    where = f"index >= '{beg_dt}' & index <= '{end_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))
    result = concat(results)
    tm.assert_frame_equal(expected, result)

