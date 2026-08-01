
def test_infer_freq_tz_transition_custom():
    index = date_range("2013-11-03", periods=5, freq="3h").tz_localize(
        "America/Chicago"
    )
    assert index.inferred_freq is None

