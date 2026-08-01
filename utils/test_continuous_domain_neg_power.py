
def test_continuous_domain_neg_power():
    assert continuous_domain((x-2)**(1-x), x, S.Reals) == Interval.open(2, oo)

