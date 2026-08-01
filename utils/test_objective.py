
def test_objective():
    assert fu(sin(x)/cos(x), measure=lambda x: x.count_ops()) == \
            tan(x)
    assert fu(sin(x)/cos(x), measure=lambda x: -x.count_ops()) == \
            sin(x)/cos(x)

