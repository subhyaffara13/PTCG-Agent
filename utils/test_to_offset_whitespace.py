
def test_to_offset_whitespace(freqstr, expected):
    result = to_offset(freqstr)
    assert result == expected

