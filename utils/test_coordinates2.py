
def test_coordinates2(temp_hdfstore):
    # get coordinates back & test vs frame
    store = temp_hdfstore

    df = DataFrame({"A": range(5), "B": range(5)})
    store.append("df", df)
    c = store.select_as_coordinates("df", ["index<3"])
    assert (c.values == np.arange(3)).all()
    result = store.select("df", where=c)
    expected = df.loc[0:2, :]
    tm.assert_frame_equal(result, expected)

    c = store.select_as_coordinates("df", ["index>=3", "index<=4"])
    assert (c.values == np.arange(2) + 3).all()
    result = store.select("df", where=c)
    expected = df.loc[3:4, :]
    tm.assert_frame_equal(result, expected)
    assert isinstance(c, Index)

