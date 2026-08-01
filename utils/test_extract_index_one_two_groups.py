
def test_extract_index_one_two_groups():
    s = Series(["a3", "b3", "d4c2"], index=["A3", "B3", "D4"], name="series_name")
    r = s.index.str.extract(r"([A-Z])", expand=True)
    e = DataFrame(["A", "B", "D"])
    tm.assert_frame_equal(r, e)

    # Prior to v0.18.0, index.str.extract(regex with one group)
    # returned Index. With more than one group, extract raised an
    # error (GH9980). Now extract always returns DataFrame.
    r = s.index.str.extract(r"(?P<letter>[A-Z])(?P<digit>[0-9])", expand=True)
    e_list = [("A", "3"), ("B", "3"), ("D", "4")]
    e = DataFrame(e_list, columns=["letter", "digit"])
    tm.assert_frame_equal(r, e)

