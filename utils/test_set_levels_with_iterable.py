
def test_set_levels_with_iterable():
    # GH23273
    sizes = [1, 2, 3]
    colors = ["black"] * 3
    index = MultiIndex.from_arrays([sizes, colors], names=["size", "color"])

    result = index.set_levels(map(int, ["3", "2", "1"]), level="size")

    expected_sizes = [3, 2, 1]
    expected = MultiIndex.from_arrays([expected_sizes, colors], names=["size", "color"])
    tm.assert_index_equal(result, expected)

