
def test_relative_risk(exposed_cases, exposed_total,
                       control_cases, control_total, expected_rr):
    result = relative_risk(exposed_cases, exposed_total,
                           control_cases, control_total)
    assert_allclose(result.relative_risk, expected_rr, rtol=1e-13)

