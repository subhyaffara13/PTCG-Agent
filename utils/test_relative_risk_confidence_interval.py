
def test_relative_risk_confidence_interval():
    result = relative_risk(exposed_cases=16, exposed_total=128,
                           control_cases=24, control_total=256)
    rr = result.relative_risk
    ci = result.confidence_interval(confidence_level=0.95)
    # The corresponding calculation in R using the epitools package.
    #
    # > library(epitools)
    # > c <- matrix(c(232, 112, 24, 16), nrow=2)
    # > result <- riskratio(c)
    # > result$measure
    #               risk ratio with 95% C.I.
    # Predictor  estimate     lower    upper
    #   Exposed1 1.000000        NA       NA
    #   Exposed2 1.333333 0.7347317 2.419628
    #
    # The last line is the result that we want.
    assert_allclose(rr, 4/3)
    assert_allclose((ci.low, ci.high), (0.7347317, 2.419628), rtol=5e-7)

