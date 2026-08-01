
def test_observed_single_column(observed):
    # https://github.com/pandas-dev/pandas/issues/8138
    d = {
        "cat": Categorical(
            ["a", "b", "a", "b"], categories=["a", "b", "c"], ordered=True
        ),
        "ints": [1, 1, 2, 2],
        "val": [10, 20, 30, 40],
    }
    df = DataFrame(d)

    groups_single_key = df.groupby("cat", observed=observed)
    result = groups_single_key.mean()

    exp_index = CategoricalIndex(
        list("ab"), name="cat", categories=list("abc"), ordered=True
    )
    expected = DataFrame({"ints": [1.5, 1.5], "val": [20.0, 30]}, index=exp_index)
    if not observed:
        index = CategoricalIndex(
            list("abc"), name="cat", categories=list("abc"), ordered=True
        )
        expected = expected.reindex(index)

    tm.assert_frame_equal(result, expected)

