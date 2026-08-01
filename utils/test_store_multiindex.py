
def test_store_multiindex(temp_hdfstore):
    # validate multi-index names
    # GH 5527

    def make_index(names=None):
        dti = date_range("2013-12-01", "2013-12-02")
        mi = MultiIndex.from_product([dti, range(2), range(3)], names=names)
        return mi

    # no names
    df = DataFrame(np.zeros((12, 2)), columns=["a", "b"], index=make_index())
    temp_hdfstore.append("df", df)
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

    # partial names
    temp_hdfstore.remove("df")
    df = DataFrame(
        np.zeros((12, 2)),
        columns=["a", "b"],
        index=make_index(["date", None, None]),
    )
    temp_hdfstore.append("df", df)
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

    # series
    ser = Series(np.zeros(12), index=make_index(["date", None, None]))
    temp_hdfstore.append("ser", ser)
    xp = Series(np.zeros(12), index=make_index(["date", "level_1", "level_2"]))
    tm.assert_series_equal(temp_hdfstore.select("ser"), xp)

    # dup with column
    temp_hdfstore.remove("df")
    df = DataFrame(
        np.zeros((12, 2)),
        columns=["a", "b"],
        index=make_index(["date", "a", "t"]),
    )
    msg = "duplicate names/columns in the multi-index when storing as a table"
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df", df)

    # dup within level
    temp_hdfstore.remove("df")
    df = DataFrame(
        np.zeros((12, 2)),
        columns=["a", "b"],
        index=make_index(["date", "date", "date"]),
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df", df)

    # fully names
    temp_hdfstore.remove("df")
    df = DataFrame(
        np.zeros((12, 2)),
        columns=["a", "b"],
        index=make_index(["date", "s", "t"]),
    )
    temp_hdfstore.append("df", df)
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

