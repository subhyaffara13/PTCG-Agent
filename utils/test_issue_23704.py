
def test_issue_23704():
    # XXX: This is testing that an exception is not raised in risch Ideally
    # manualintegrate (manual=True) would be able to compute this but
    # manualintegrate is very slow for this example so we don't test that here.
    assert (integrate(log(x)/x**2/(c*x**2+b*x+a),x, risch=True)
        == NonElementaryIntegral(log(x)/(a*x**2 + b*x**3 + c*x**4), x))

