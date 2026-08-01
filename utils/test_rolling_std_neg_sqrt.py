
def test_rolling_std_neg_sqrt():
    # unit test from Bottleneck

    # Test move_nanstd for neg sqrt.

    a = Series(
        [
            0.0011448196318903589,
            0.00028718669878572767,
            0.00028718669878572767,
            0.00028718669878572767,
            0.00028718669878572767,
        ]
    )
    b = a.rolling(window=3).std()
    assert np.isfinite(b[2:]).all()

    b = a.ewm(span=3).std()
    assert np.isfinite(b[2:]).all()

