
def test_unobserved_in_index(keys, expected_values, expected_index_levels, test_series):
    # GH#49354 - ensure unobserved cats occur when grouping by index levels
    df = DataFrame(
        {
            "a": Categorical([1, 1, 2], categories=[1, 2, 3]),
            "a2": Categorical([1, 1, 2], categories=[1, 2, 3]),
            "b": [4, 5, 6],
            "c": [7, 8, 9],
        }
    ).set_index(["a", "a2"])
    if "b" not in keys:
        # Only keep b when it is used for grouping for consistent columns in the result
        df = df.drop(columns="b")

    gb = df.groupby(keys, observed=False)
    if test_series:
        gb = gb["c"]
    result = gb.sum()

    if len(keys) == 1:
        index = expected_index_levels
    else:
        codes = [[0, 0, 0, 1, 1, 1, 2, 2, 2], 3 * [0, 1, 2]]
        index = MultiIndex(
            expected_index_levels,
            codes=codes,
            names=keys,
        )
    expected = DataFrame({"c": expected_values}, index=index)
    if test_series:
        expected = expected["c"]
    tm.assert_equal(result, expected)

