
def test_continuous_domain_gamma():
    assert continuous_domain(gamma(x), x, S.Reals).contains(-1) == False

