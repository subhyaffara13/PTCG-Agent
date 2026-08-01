
def test_to_offset_negative(freqstr, expected):
    result = to_offset(freqstr)
    assert result.n == expected

