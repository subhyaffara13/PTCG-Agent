
def test_issue_10801():
    # make sure limits work with binomial
    assert limit(16**k / (k * binomial(2*k, k)**2), k, oo) == pi

