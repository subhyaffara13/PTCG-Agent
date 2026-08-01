
def test_union_same_value_duplicated_in_both():
    # GH#36289
    a = Index([0, 0, 1])
    b = Index([0, 0, 1, 2])
    result = a.union(b)
    expected = Index([0, 0, 1, 2])
    tm.assert_index_equal(result, expected)

