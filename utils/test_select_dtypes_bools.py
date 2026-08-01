
def test_select_dtypes_bools(temp_hdfstore):
    # bool columns (GH #2849)
    df = DataFrame(np.random.default_rng(2).standard_normal((5, 2)), columns=["A", "B"])
    df["object"] = "foo"
    df.loc[4:5, "object"] = "bar"
    df["boolv"] = df["A"] > 0
    temp_hdfstore.append("df", df, data_columns=True)

    expected = df[df.boolv == True].reindex(columns=["A", "boolv"])  # noqa: E712
    for v in [True, "true", 1]:
        result = temp_hdfstore.select("df", f"boolv == {v}", columns=["A", "boolv"])
        tm.assert_frame_equal(expected, result)

    expected = df[df.boolv == False].reindex(columns=["A", "boolv"])  # noqa: E712
    for v in [False, "false", 0]:
        result = temp_hdfstore.select("df", f"boolv == {v}", columns=["A", "boolv"])
        tm.assert_frame_equal(expected, result)

