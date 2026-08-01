
def test_issue_4891():
    # Requires the hypergeometric function.
    assert not integrate(cos(x)**y, x).has(Integral)

