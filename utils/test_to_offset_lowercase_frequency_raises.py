
def test_to_offset_lowercase_frequency_raises(freq_depr):
    msg = f"Invalid frequency: {freq_depr}"

    with pytest.raises(ValueError, match=msg):
        to_offset(freq_depr)

