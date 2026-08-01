
def test_replace_list_inplace_refs_categorical():
    df = DataFrame({"a": ["a", "b", "c"]}, dtype="category")
    view = df[:]
    df_orig = df.copy()
    df.replace(["c"], value="a", inplace=True)
    tm.assert_frame_equal(df_orig, view)

