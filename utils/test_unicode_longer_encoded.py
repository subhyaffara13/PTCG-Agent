
def test_unicode_longer_encoded(temp_hdfstore):
    # GH 11234
    char = "\u0394"
    df = DataFrame({"A": [char]})
    temp_hdfstore.put("df", df, format="table", encoding="utf-8")
    result = temp_hdfstore.get("df")
    tm.assert_frame_equal(result, df)

    df = DataFrame({"A": ["a", char], "B": ["b", "b"]})
    temp_hdfstore.remove("df")
    temp_hdfstore.put("df", df, format="table", encoding="utf-8")
    result = temp_hdfstore.get("df")
    tm.assert_frame_equal(result, df)

