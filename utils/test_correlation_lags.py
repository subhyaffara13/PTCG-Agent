
def test_correlation_lags(mode, behind, input_size, xp):
    # generate random data
    rng = np.random.RandomState(0)
    in1 = rng.standard_normal(input_size)
    offset = int(input_size/10)
    # generate offset version of array to correlate with
    if behind:
        # y is behind x
        in2 = np.concatenate([rng.standard_normal(offset), in1])
        expected = -offset
    else:
        # y is ahead of x
        in2 = in1[offset:]
        expected = offset
    # cross correlate, returning lag information
    correlation = correlate(in1, in2, mode=mode)
    lags = correlation_lags(in1.size, in2.size, mode=mode)
    # identify the peak
    lag_index = np.argmax(correlation)
    # Check as expected
    xp_assert_equal(lags[lag_index], expected)
    # Correlation and lags shape should match
    assert lags.shape == correlation.shape

