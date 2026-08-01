
def test_intersection_mutation_safety():
    # GH#63169
    index1 = Index([0, 1], name="original")
    index2 = Index([0, 1], name="original")

    result = index1.intersection(index2)

    assert result is not index1
    assert result is not index2

    tm.assert_index_equal(result, index1)
    assert result.name == "original"

    index1.name = "changed"

    assert result.name == "original"
    assert index1.name == "changed"

