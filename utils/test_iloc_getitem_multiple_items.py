
def test_iloc_getitem_multiple_items():
    # GH 5528
    tup = zip(*[["a", "a", "b", "b"], ["x", "y", "x", "y"]])
    index = MultiIndex.from_tuples(tup)
    df = DataFrame(np.random.default_rng(2).standard_normal((4, 4)), index=index)
    result = df.iloc[[2, 3]]
    expected = df.xs("b", drop_level=False)
    tm.assert_frame_equal(result, expected)

