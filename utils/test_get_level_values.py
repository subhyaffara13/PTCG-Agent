
def test_get_level_values(idx):
    result = idx.get_level_values(0)
    expected = Index(["foo", "foo", "bar", "baz", "qux", "qux"], name="first")
    tm.assert_index_equal(result, expected)
    assert result.name == "first"

    result = idx.get_level_values("first")
    expected = idx.get_level_values(0)
    tm.assert_index_equal(result, expected)

    # GH 10460
    index = MultiIndex(
        levels=[CategoricalIndex(["A", "B"]), CategoricalIndex([1, 2, 3])],
        codes=[np.array([0, 0, 0, 1, 1, 1]), np.array([0, 1, 2, 0, 1, 2])],
    )

    exp = CategoricalIndex(["A", "A", "A", "B", "B", "B"])
    tm.assert_index_equal(index.get_level_values(0), exp)
    exp = CategoricalIndex([1, 2, 3, 1, 2, 3])
    tm.assert_index_equal(index.get_level_values(1), exp)

