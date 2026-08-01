
def test_as_index():
    # GH13204
    df = DataFrame(
        {
            "cat": Categorical([1, 2, 2], [1, 2, 3]),
            "A": [10, 11, 11],
            "B": [101, 102, 103],
        }
    )
    result = df.groupby(["cat", "A"], as_index=False, observed=True).sum()
    expected = DataFrame(
        {
            "cat": Categorical([1, 2], categories=df.cat.cat.categories),
            "A": [10, 11],
            "B": [101, 205],
        },
        columns=["cat", "A", "B"],
    )
    tm.assert_frame_equal(result, expected)

    # function grouper
    f = lambda r: df.loc[r, "A"]
    result = df.groupby(["cat", f], as_index=False, observed=True).sum()
    expected = DataFrame(
        {
            "cat": Categorical([1, 2], categories=df.cat.cat.categories),
            "level_1": [10, 11],
            "A": [10, 22],
            "B": [101, 205],
        },
    )
    tm.assert_frame_equal(result, expected)

    # another not in-axis grouper (conflicting names in index)
    s = Series(["a", "b", "b"], name="cat")
    result = df.groupby(["cat", s], as_index=False, observed=True).sum()
    expected = DataFrame(
        {
            "cat": ["a", "b"],
            "A": [10, 22],
            "B": [101, 205],
        },
    )
    tm.assert_frame_equal(result, expected)

    # is original index dropped?
    group_columns = ["cat", "A"]
    expected = DataFrame(
        {
            "cat": Categorical([1, 2], categories=df.cat.cat.categories),
            "A": [10, 11],
            "B": [101, 205],
        },
        columns=["cat", "A", "B"],
    )

    for name in [None, "X", "B"]:
        df.index = Index(list("abc"), name=name)
        result = df.groupby(group_columns, as_index=False, observed=True).sum()

        tm.assert_frame_equal(result, expected)


def test_as_index(slice_test_df, arg, expected_rows):
    # Test the default as_index behaviour
    result = slice_test_df.groupby("Group", sort=False)._positional_selector[arg]
    expected = slice_test_df.iloc[expected_rows]

    tm.assert_frame_equal(result, expected)

