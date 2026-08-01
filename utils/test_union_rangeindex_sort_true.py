
def test_union_rangeindex_sort_true():
    # GH 53490
    idx1 = RangeIndex(1, 100, 6)
    idx2 = RangeIndex(1, 50, 3)
    result = idx1.union(idx2, sort=True)
    expected = Index(
        [
            1,
            4,
            7,
            10,
            13,
            16,
            19,
            22,
            25,
            28,
            31,
            34,
            37,
            40,
            43,
            46,
            49,
            55,
            61,
            67,
            73,
            79,
            85,
            91,
            97,
        ]
    )
    tm.assert_index_equal(result, expected)

