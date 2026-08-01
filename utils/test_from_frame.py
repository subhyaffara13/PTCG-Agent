
def test_from_frame():
    # GH 22420
    df = pd.DataFrame(
        [["a", "a"], ["a", "b"], ["b", "a"], ["b", "b"]], columns=["L1", "L2"]
    )
    expected = MultiIndex.from_tuples(
        [("a", "a"), ("a", "b"), ("b", "a"), ("b", "b")], names=["L1", "L2"]
    )
    result = MultiIndex.from_frame(df)
    tm.assert_index_equal(expected, result)

