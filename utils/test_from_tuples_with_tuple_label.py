
def test_from_tuples_with_tuple_label():
    # GH 15457
    expected = pd.DataFrame(
        [[2, 1, 2], [4, (1, 2), 3]], columns=["a", "b", "c"]
    ).set_index(["a", "b"])
    idx = MultiIndex.from_tuples([(2, 1), (4, (1, 2))], names=("a", "b"))
    result = pd.DataFrame([2, 3], columns=["c"], index=idx)
    tm.assert_frame_equal(expected, result)

