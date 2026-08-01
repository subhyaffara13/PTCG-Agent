
def test_groupby_dropna_with_multiindex_input(input_index, keys, series):
    # GH#46783
    obj = pd.DataFrame(
        {
            "a": [1, np.nan],
            "b": [1, 1],
            "c": [2, 3],
        }
    )

    expected = obj.set_index(keys)
    if series:
        expected = expected["c"]
    elif input_index == ["a", "b"] and keys == ["a"]:
        # Column b should not be aggregated
        expected = expected[["c"]]

    if input_index is not None:
        obj = obj.set_index(input_index)
    gb = obj.groupby(keys, dropna=False)
    if series:
        gb = gb["c"]
    result = gb.sum()

    tm.assert_equal(result, expected)

