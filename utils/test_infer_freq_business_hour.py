
def test_infer_freq_business_hour(data, expected):
    # see gh-7905
    idx = DatetimeIndex(data)
    assert idx.inferred_freq == expected

