
def test_describe_non_cython_paths():
    # GH#5610 non-cython calls should not include the grouper
    # Tests for code not expected to go through cython paths.
    df = DataFrame(
        [[1, 2, "foo"], [1, np.nan, "bar"], [3, np.nan, "baz"]],
        columns=["A", "B", "C"],
    )
    gb = df.groupby("A")
    expected_index = Index([1, 3], name="A")
    expected_col = MultiIndex(
        levels=[["B"], ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]],
        codes=[[0] * 8, list(range(8))],
    )
    expected = DataFrame(
        [
            [1.0, 2.0, np.nan, 2.0, 2.0, 2.0, 2.0, 2.0],
            [0.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        ],
        index=expected_index,
        columns=expected_col,
    )
    result = gb.describe()
    tm.assert_frame_equal(result, expected)

    gni = df.groupby("A", as_index=False)
    expected = expected.reset_index()
    result = gni.describe()
    tm.assert_frame_equal(result, expected)

