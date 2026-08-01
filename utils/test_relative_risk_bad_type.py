
def test_relative_risk_bad_type():
    with pytest.raises(TypeError, match="must be an integer"):
        relative_risk(1, 10, 2.0, 40)

