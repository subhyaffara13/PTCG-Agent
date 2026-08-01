
def test_issue_4212():
    # XXX: Maybe this should be expected to fail without real assumptions on x.
    # As a complex function sign(x) is not analytic and so there is no complex
    # function whose complex derivative is sign(x). With real assumptions this
    # works (see test_issue_4212_real above).
    assert not integrate(sign(x), x).has(Integral)

