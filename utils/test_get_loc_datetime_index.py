
def test_get_loc_datetime_index():
    # GH#24263
    index = pd.date_range("2001-01-01", periods=100)
    mi = MultiIndex.from_arrays([index])
    # Check if get_loc matches for Index and MultiIndex
    assert mi.get_loc("2001-01") == slice(0, 31, None)
    assert index.get_loc("2001-01") == slice(0, 31, None)

    loc = mi[::2].get_loc("2001-01")
    expected = index[::2].get_loc("2001-01")
    assert loc == expected

    loc = mi.repeat(2).get_loc("2001-01")
    expected = index.repeat(2).get_loc("2001-01")
    assert loc == expected

    loc = mi.append(mi).get_loc("2001-01")
    expected = index.append(index).get_loc("2001-01")
    # TODO: standardize return type for MultiIndex.get_loc
    tm.assert_numpy_array_equal(loc.nonzero()[0], expected)

