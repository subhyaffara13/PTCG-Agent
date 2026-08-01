
def test_polylog_manual():
    # Make sure _parts_rule does not go into an infinite loop here
    assert not integrate(log(1/x)/(x + 1), x, manual=True).has(Integral)

