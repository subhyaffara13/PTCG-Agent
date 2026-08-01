
def test_consistent_coerce_for_shapes(lst):
    # we want column names to NOT be propagated
    # just because the shape matches the input shape
    df = DataFrame(
        np.random.default_rng(2).standard_normal((4, 3)), columns=["A", "B", "C"]
    )

    result = df.apply(lambda x: lst, axis=1)
    expected = Series([lst for t in df.itertuples()])
    tm.assert_series_equal(result, expected)

