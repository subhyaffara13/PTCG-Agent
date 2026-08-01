
def test_issue_14375():
    # This raised a TypeError. The antiderivative has exp_polar, which
    # may be possible to unpolarify, so the exact output is not asserted here.
    assert integrate(exp(I*x)*log(x), x).has(Ei)

