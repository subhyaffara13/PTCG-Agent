
def test_negone_ordinals():
    freqs = ["Y", "M", "Q", "D", "h", "min", "s"]

    period = Period(ordinal=-1, freq="D")
    for freq in freqs:
        repr(period.asfreq(freq))

    for freq in freqs:
        period = Period(ordinal=-1, freq=freq)
        repr(period)
        assert period.year == 1969

    with tm.assert_produces_warning(FutureWarning, match=bday_msg):
        period = Period(ordinal=-1, freq="B")
    repr(period)
    period = Period(ordinal=-1, freq="W")
    repr(period)

