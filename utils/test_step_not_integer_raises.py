
def test_step_not_integer_raises():
    with pytest.raises(ValueError, match="step must be an integer"):
        DataFrame(range(2)).rolling(1, step="foo")

