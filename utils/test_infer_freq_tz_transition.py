
def test_infer_freq_tz_transition(tz_naive_fixture, date_pair, freq):
    # see gh-8772
    tz = tz_naive_fixture
    idx = date_range(date_pair[0], date_pair[1], freq=freq, tz=tz)
    assert idx.inferred_freq == freq

