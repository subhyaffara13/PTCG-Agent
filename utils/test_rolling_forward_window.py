
def test_rolling_forward_window(
    frame_or_series, func, np_func, expected, np_kwargs, step
):
    # GH 32865
    values = np.arange(10.0)
    values[5] = 100.0

    indexer = FixedForwardWindowIndexer(window_size=3)

    match = "Forward-looking windows can't have center=True"
    rolling = frame_or_series(values).rolling(window=indexer, center=True)
    with pytest.raises(ValueError, match=match):
        getattr(rolling, func)()

    match = "Forward-looking windows don't support setting the closed argument"
    rolling = frame_or_series(values).rolling(window=indexer, closed="right")
    with pytest.raises(ValueError, match=match):
        getattr(rolling, func)()

    rolling = frame_or_series(values).rolling(window=indexer, min_periods=2, step=step)
    result = getattr(rolling, func)()

    # Check that the function output matches the explicitly provided array
    expected = frame_or_series(expected)[::step]
    tm.assert_equal(result, expected)

    # Check that the rolling function output matches applying an alternative
    # function to the rolling window object
    expected2 = frame_or_series(rolling.apply(lambda x: np_func(x, **np_kwargs)))
    tm.assert_equal(result, expected2)

    # Check that the function output matches applying an alternative function
    # if min_periods isn't specified
    # GH 39604: After count-min_periods deprecation, apply(lambda x: len(x))
    # is equivalent to count after setting min_periods=0
    min_periods = 0 if func == "count" else None
    rolling3 = frame_or_series(values).rolling(window=indexer, min_periods=min_periods)
    result3 = getattr(rolling3, func)()
    expected3 = frame_or_series(rolling3.apply(lambda x: np_func(x, **np_kwargs)))
    tm.assert_equal(result3, expected3)

