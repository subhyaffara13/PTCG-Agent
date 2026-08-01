
def test_to_offset_uppercase_frequency_raises(freq):
    msg = f"Invalid frequency: {freq}"

    with pytest.raises(ValueError, match=msg):
        to_offset(freq)

