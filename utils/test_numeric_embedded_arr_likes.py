
def test_numeric_embedded_arr_likes(data, exp_data):
    # Test to_numeric with embedded lists and arrays
    df = DataFrame({"a": data})
    df["a"] = df["a"].apply(to_numeric)

    expected = DataFrame({"a": exp_data})
    tm.assert_frame_equal(df, expected)

