
def test_add_new_column_infer_string():
    # GH#55366
    df = DataFrame({"x": [1]})
    with pd.option_context("future.infer_string", True):
        df.loc[df["x"] == 1, "y"] = "1"
    expected = DataFrame(
        {"x": [1], "y": Series(["1"], dtype=pd.StringDtype(na_value=np.nan))},
        columns=Index(["x", "y"], dtype="str"),
    )
    tm.assert_frame_equal(df, expected)

