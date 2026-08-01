
def test_infer_freq_pyarrow():
    # GH#58403
    data = ["2022-01-01T10:00:00", "2022-01-01T10:00:30", "2022-01-01T10:01:00"]
    pd_series = Series(data).astype("timestamp[s][pyarrow]")
    pd_index = Index(data).astype("timestamp[s][pyarrow]")

    assert frequencies.infer_freq(pd_index.values) == "30s"
    assert frequencies.infer_freq(pd_series.values) == "30s"
    assert frequencies.infer_freq(pd_index) == "30s"
    assert frequencies.infer_freq(pd_series) == "30s"

