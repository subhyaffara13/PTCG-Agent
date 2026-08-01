
def test_multiindex_intersection_mutation_safety():
    # GH#63169
    mi1 = MultiIndex.from_tuples([("a", 1), ("b", 2)], names=["x", "y"])
    mi2 = MultiIndex.from_tuples([("a", 1), ("b", 2)], names=["x", "y"])

    result = mi1.intersection(mi2)
    assert result is not mi1

    mi1.names = ["changed1", "changed2"]
    assert result.names == ["x", "y"]

