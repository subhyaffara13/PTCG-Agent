
def test_select_iterator_many_empty_frames(temp_hdfstore):
    # GH 8014
    # using iterator and where clause can return many empty
    # frames.
    chunksize = 10_000

    # with iterator, range limited to the first chunk
    expected = DataFrame(
        np.random.default_rng(2).standard_normal((100064, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=100064, freq="s", unit="ns"),
    )
    temp_hdfstore.append("df", expected)

    beg_dt = expected.index[0]
    end_dt = expected.index[chunksize - 1]

    # select w/iterator and where clause, single term, begin of range
    where = f"index >= '{beg_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))
    result = concat(results)
    rexpected = expected[expected.index >= beg_dt]
    tm.assert_frame_equal(rexpected, result)

    # select w/iterator and where clause, single term, end of range
    where = f"index <= '{end_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))

    assert len(results) == 1
    result = concat(results)
    rexpected = expected[expected.index <= end_dt]
    tm.assert_frame_equal(rexpected, result)

    # select w/iterator and where clause, inclusive range
    where = f"index >= '{beg_dt}' & index <= '{end_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))

    # should be 1, is 10
    assert len(results) == 1
    result = concat(results)
    rexpected = expected[(expected.index >= beg_dt) & (expected.index <= end_dt)]
    tm.assert_frame_equal(rexpected, result)

    # select w/iterator and where clause which selects
    # *nothing*.
    #
    # To be consistent with Python idiom I suggest this should
    # return [] e.g. `for e in []: print True` never prints
    # True.

    where = f"index <= '{beg_dt}' & index >= '{end_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))

    # should be []
    assert len(results) == 0

