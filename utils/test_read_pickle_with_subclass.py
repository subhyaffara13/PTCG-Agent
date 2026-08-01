
def test_read_pickle_with_subclass(temp_file):
    # GH 12163
    expected = Series(dtype=object), MyTz()
    result = tm.round_trip_pickle(expected, temp_file)

    tm.assert_series_equal(result[0], expected[0])
    assert isinstance(result[1], MyTz)

