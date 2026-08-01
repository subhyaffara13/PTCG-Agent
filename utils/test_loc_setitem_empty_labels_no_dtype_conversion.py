
def test_loc_setitem_empty_labels_no_dtype_conversion():
    # GH 29707

    df = pd.DataFrame({"a": [2, 3]})
    expected = df.copy()
    assert df.a.dtype == "int64"
    df.loc[[]] = 0.1

    assert df.a.dtype == "int64"
    tm.assert_frame_equal(df, expected)

