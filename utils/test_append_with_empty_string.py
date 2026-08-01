
def test_append_with_empty_string(temp_hdfstore):
    # with all empty strings (GH 12242)
    df = DataFrame({"x": ["a", "b", "c", "d", "e", "f", ""]})
    temp_hdfstore.append("df", df[:-1], min_itemsize={"x": 1})
    temp_hdfstore.append("df", df[-1:], min_itemsize={"x": 1})
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

