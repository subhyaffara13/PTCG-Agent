
def test_stack_sort_false_multi_level(future_stack):
    # GH 15105
    idx = MultiIndex.from_tuples([("weight", "kg"), ("height", "m")])
    df = DataFrame([[1.0, 2.0], [3.0, 4.0]], index=["cat", "dog"], columns=idx)
    kwargs = {} if future_stack else {"sort": False}
    result = df.stack([0, 1], future_stack=future_stack, **kwargs)
    expected_index = MultiIndex.from_tuples(
        [
            ("cat", "weight", "kg"),
            ("cat", "height", "m"),
            ("dog", "weight", "kg"),
            ("dog", "height", "m"),
        ]
    )
    expected = Series([1.0, 2.0, 3.0, 4.0], index=expected_index)
    tm.assert_series_equal(result, expected)

