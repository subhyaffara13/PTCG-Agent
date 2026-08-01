
def test_relative_risk_ci_edge_cases_01():
    result = relative_risk(exposed_cases=0, exposed_total=12,
                           control_cases=1, control_total=30)
    assert_equal(result.relative_risk, 0)
    ci = result.confidence_interval()
    assert_equal((ci.low, ci.high), (0.0, np.nan))

