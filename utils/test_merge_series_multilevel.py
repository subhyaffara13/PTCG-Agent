
def test_merge_series_multilevel():
    # GH#47946
    # GH 40993: For raising, enforced in 2.0
    a = DataFrame(
        {"A": [1, 2, 3, 4]},
        index=MultiIndex.from_product([["a", "b"], [0, 1]], names=["outer", "inner"]),
    )
    b = Series(
        [1, 2, 3, 4],
        index=MultiIndex.from_product([["a", "b"], [1, 2]], names=["outer", "inner"]),
        name=("B", "C"),
    )
    with pytest.raises(
        MergeError, match="Not allowed to merge between different levels"
    ):
        merge(a, b, on=["outer", "inner"])

