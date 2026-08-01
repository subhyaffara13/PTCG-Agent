
def test_correlation_lags_invalid_mode(xp):
    with pytest.raises(ValueError, match="Mode asdfgh is invalid"):
        correlation_lags(100, 100, mode="asdfgh")

