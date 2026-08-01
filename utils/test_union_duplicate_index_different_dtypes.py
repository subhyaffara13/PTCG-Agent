
def test_union_duplicate_index_different_dtypes():
    # GH#36289
    a = Index([1, 2, 2, 3])
    b = Index(["1", "0", "0"])
    expected = Index([1, 2, 2, 3, "1", "0", "0"])
    result = a.union(b, sort=False)
    tm.assert_index_equal(result, expected)

