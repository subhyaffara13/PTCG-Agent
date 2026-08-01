
def test_from_tuples_iterator():
    # GH 18434
    # input iterator for tuples
    expected = MultiIndex(
        levels=[[1, 3], [2, 4]], codes=[[0, 1], [0, 1]], names=["a", "b"]
    )

    result = MultiIndex.from_tuples(zip([1, 3], [2, 4], strict=True), names=["a", "b"])
    tm.assert_index_equal(result, expected)

    # input non-iterables
    msg = "Input must be a list / sequence of tuple-likes."
    with pytest.raises(TypeError, match=msg):
        MultiIndex.from_tuples(0)

