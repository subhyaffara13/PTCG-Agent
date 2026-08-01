
def test_infer_freq_custom(base_delta_code_pair, constructor):
    b = Timestamp(datetime.now())
    base_delta, _ = base_delta_code_pair

    index = constructor(b, base_delta)
    assert frequencies.infer_freq(index) is None

