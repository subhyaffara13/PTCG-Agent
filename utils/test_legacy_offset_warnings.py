
def test_legacy_offset_warnings(offset_func, freq):
    with pytest.raises(ValueError, match=INVALID_FREQ_ERR_MSG):
        offset_func(freq)

