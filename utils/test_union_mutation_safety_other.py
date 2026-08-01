
def test_union_mutation_safety_other():
    # GH#63169
    index1 = Index([0, 1], name="original")
    index2 = Index([0, 1], name="original")

    result = index1.union(index2)

    assert result is not index2

    tm.assert_index_equal(result, index2)
    assert result.name == "original"

    index2.name = "changed"

    assert result.name == "original"
    assert index2.name == "changed"

