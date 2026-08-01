
def test_relative_risk_ci_conflevel1():
    result = relative_risk(exposed_cases=4, exposed_total=12,
                           control_cases=5, control_total=30)
    ci = result.confidence_interval(1)
    assert_equal((ci.low, ci.high), (0, np.inf))

