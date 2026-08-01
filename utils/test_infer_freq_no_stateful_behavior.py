
def test_infer_freq_no_stateful_behavior():
    # GH#55794 infer_freq should not have stateful behavior
    # calling infer_freq on a full index with duplicates should not
    # affect the result of calling it on a slice without duplicates
    times = to_datetime(["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-03"])

    # Before calling infer_freq on full index
    assert frequencies.infer_freq(times[:3]) == "D"

    # Call on full index (which has duplicates, so returns None)
    assert frequencies.infer_freq(times) is None

    # After calling on full index, slice should still return "D"
    assert frequencies.infer_freq(times[:3]) == "D"

