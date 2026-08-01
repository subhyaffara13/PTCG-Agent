
def test_select_iterator_non_complete_8014(temp_hdfstore):
    # GH 8014
    # using iterator and where clause
    chunksize = 1e4

    # with iterator, non complete range
    expected = DataFrame(
        np.random.default_rng(2).standard_normal((100064, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=100064, freq="s", unit="ns"),
    )
    temp_hdfstore.append("df", expected)

    beg_dt = expected.index[1]
    end_dt = expected.index[-2]

    # select w/iterator and where clause, single term, begin of range
    where = f"index >= '{beg_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))
    result = concat(results)
    rexpected = expected[expected.index >= beg_dt]
    tm.assert_frame_equal(rexpected, result)

    # select w/iterator and where clause, single term, end of range
    where = f"index <= '{end_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))
    result = concat(results)
    rexpected = expected[expected.index <= end_dt]
    tm.assert_frame_equal(rexpected, result)

    # select w/iterator and where clause, inclusive range
    where = f"index >= '{beg_dt}' & index <= '{end_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))
    result = concat(results)
    rexpected = expected[(expected.index >= beg_dt) & (expected.index <= end_dt)]
    tm.assert_frame_equal(rexpected, result)

