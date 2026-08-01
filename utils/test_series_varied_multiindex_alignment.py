
def test_series_varied_multiindex_alignment():
    # GH 20414
    s1 = Series(
        range(8),
        index=pd.MultiIndex.from_product(
            [list("ab"), list("xy"), [1, 2]], names=["ab", "xy", "num"]
        ),
    )
    s2 = Series(
        [1000 * i for i in range(1, 5)],
        index=pd.MultiIndex.from_product([list("xy"), [1, 2]], names=["xy", "num"]),
    )
    result = s1.loc[pd.IndexSlice[["a"], :, :]] + s2
    expected = Series(
        [1000, 2001, 3002, 4003],
        index=pd.MultiIndex.from_tuples(
            [("a", "x", 1), ("a", "x", 2), ("a", "y", 1), ("a", "y", 2)],
            names=["ab", "xy", "num"],
        ),
    )
    tm.assert_series_equal(result, expected)

