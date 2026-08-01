
def test_relative_risk_bad_value(ec, et, cc, ct):
    with pytest.raises(ValueError, match="must be an integer not less than"):
        relative_risk(ec, et, cc, ct)

