
def test_intersect_with_duplicates(tuples, exp_tuples):
    # GH#36915
    left = MultiIndex.from_tuples(tuples, names=["first", "second"])
    right = MultiIndex.from_tuples(
        [("val1", "test1"), ("val1", "test1"), ("val2", "test2")],
        names=["first", "second"],
    )
    result = left.intersection(right)
    expected = MultiIndex.from_tuples(exp_tuples, names=["first", "second"])
    tm.assert_index_equal(result, expected)

