
def test_loc_with_nan():
    # GH: 27104
    df = DataFrame(
        {"col": [1, 2, 5], "ind1": ["a", "d", np.nan], "ind2": [1, 4, 5]}
    ).set_index(["ind1", "ind2"])
    result = df.loc[["a"]]
    expected = DataFrame(
        {"col": [1]}, index=MultiIndex.from_tuples([("a", 1)], names=["ind1", "ind2"])
    )
    tm.assert_frame_equal(result, expected)

    result = df.loc["a"]
    expected = DataFrame({"col": [1]}, index=Index([1], name="ind2"))
    tm.assert_frame_equal(result, expected)

