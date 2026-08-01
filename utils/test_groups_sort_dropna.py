
def test_groups_sort_dropna(sort, dropna):
    # GH#56966, GH#56851
    df = DataFrame([[2.0, 1.0], [np.nan, 4.0], [0.0, 3.0]])
    keys = [(2.0, 1.0), (np.nan, 4.0), (0.0, 3.0)]
    values = [
        RangeIndex(0, 1),
        RangeIndex(1, 2),
        RangeIndex(2, 3),
    ]
    if sort:
        taker = [2, 0] if dropna else [2, 0, 1]
    else:
        taker = [0, 2] if dropna else [0, 1, 2]
    expected = {keys[idx]: values[idx] for idx in taker}

    gb = df.groupby([0, 1], sort=sort, dropna=dropna)
    result = gb.groups

    for result_key, expected_key in zip(result.keys(), expected.keys(), strict=True):
        # Compare as NumPy arrays to handle np.nan
        result_key = np.array(result_key)
        expected_key = np.array(expected_key)
        tm.assert_numpy_array_equal(result_key, expected_key)
    for result_value, expected_value in zip(
        result.values(), expected.values(), strict=True
    ):
        tm.assert_index_equal(result_value, expected_value)

