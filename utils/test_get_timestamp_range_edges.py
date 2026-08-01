
def test_get_timestamp_range_edges(first, last, freq, exp_first, exp_last, unit):
    first = Period(first)
    first = first.to_timestamp(first.freq).as_unit(unit)
    last = Period(last)
    last = last.to_timestamp(last.freq).as_unit(unit)

    exp_first = Timestamp(exp_first)
    exp_last = Timestamp(exp_last)

    freq = pd.tseries.frequencies.to_offset(freq)
    result = _get_timestamp_range_edges(first, last, freq, unit="ns")
    expected = (exp_first, exp_last)
    assert result == expected

