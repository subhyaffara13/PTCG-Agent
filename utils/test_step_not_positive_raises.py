
def test_step_not_positive_raises():
    with pytest.raises(ValueError, match="step must be >= 0"):
        DataFrame(range(2)).rolling(1, step=-1)

