
def test_index():
    G = PermutationGroup(Permutation(0,1,2), Permutation(0,2,3))
    H = G.subgroup([Permutation(0,1,3)])
    assert G.index(H) == 4


def test_index(method, sub, start, end, index_or_series, any_string_dtype, expected):
    obj = index_or_series(
        ["ABCDEFG", "BCDEFEF", "DEFGHIJEF", "EFGHEF"], dtype=any_string_dtype
    )
    expected_dtype = (
        np.int64 if is_object_or_nan_string_dtype(any_string_dtype) else "Int64"
    )
    expected = index_or_series(expected, dtype=expected_dtype)

    result = getattr(obj.str, method)(sub, start, end)

    if index_or_series is Series:
        tm.assert_series_equal(result, expected)
    else:
        tm.assert_index_equal(result, expected)

    # compare with standard library
    expected = [getattr(item, method)(sub, start, end) for item in obj]
    assert list(result) == expected


def test_index(index):
    # GH 32667

    df = pd.DataFrame([1, 2, 3])

    result = df.to_markdown(index=index)

    if index:
        expected = (
            "|    |   0 |\n|---:|----:|\n|  0 |   1 |\n|  1 |   2 |\n|  2 |   3 |"
        )
    else:
        expected = "|   0 |\n|----:|\n|   1 |\n|   2 |\n|   3 |"
    assert result == expected

