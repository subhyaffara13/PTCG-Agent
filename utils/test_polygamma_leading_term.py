
def test_polygamma_leading_term():
    expr = -log(1/x) + polygamma(0, 1 + 1/x) + S.EulerGamma
    assert expr.as_leading_term(x, logx=-y) == S.EulerGamma

