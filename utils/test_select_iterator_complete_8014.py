
def test_select_iterator_complete_8014(temp_hdfstore):
    # GH 8014
    # using iterator and where clause
    # no iterator
    expected = DataFrame(
        np.random.default_rng(2).standard_normal((100064, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=100064, freq="s", unit="ns"),
    )
    temp_hdfstore.append("df", expected)

    beg_dt = expected.index[0]
    end_dt = expected.index[-1]

    # select w/o iteration and no where clause works
    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(expected, result)

    # select w/o iterator and where clause, single term, begin
    # of range, works
    where = f"index >= '{beg_dt}'"
    result = temp_hdfstore.select("df", where=where)
    tm.assert_frame_equal(expected, result)

    # select w/o iterator and where clause, single term, end
    # of range, works
    where = f"index <= '{end_dt}'"
    result = temp_hdfstore.select("df", where=where)
    tm.assert_frame_equal(expected, result)

    # select w/o iterator and where clause, inclusive range,
    # works
    where = f"index >= '{beg_dt}' & index <= '{end_dt}'"
    result = temp_hdfstore.select("df", where=where)
    tm.assert_frame_equal(expected, result)

