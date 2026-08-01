
def test_relative_risk_ci_edge_cases_00():
    result = relative_risk(exposed_cases=0, exposed_total=12,
                           control_cases=0, control_total=30)
    assert_equal(result.relative_risk, np.nan)
    ci = result.confidence_interval()
    assert_equal((ci.low, ci.high), (np.nan, np.nan))

