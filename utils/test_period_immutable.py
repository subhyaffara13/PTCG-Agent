
def test_period_immutable():
    # see gh-17116
    msg = "not writable"

    per = Period("2014Q1")
    with pytest.raises(AttributeError, match=msg):
        per.ordinal = 14

    freq = per.freq
    with pytest.raises(AttributeError, match=msg):
        per.freq = 2 * freq

