
def test_nan_selection_bug_4858(temp_hdfstore):
    df = DataFrame({"cols": range(6), "values": range(6)}, dtype="float64")
    df["cols"] = (df["cols"] + 10).apply(str)
    df.iloc[0] = np.nan

    expected = DataFrame(
        {"cols": ["13.0", "14.0", "15.0"], "values": [3.0, 4.0, 5.0]},
        index=[3, 4, 5],
    )

    # write w/o the index on that particular column
    temp_hdfstore.append("df", df, data_columns=True, index=["cols"])
    result = temp_hdfstore.select("df", where="values>2.0")
    tm.assert_frame_equal(result, expected)

