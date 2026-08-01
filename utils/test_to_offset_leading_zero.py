
def test_to_offset_leading_zero(freqstr, expected):
    result = to_offset(freqstr)
    assert result.n == expected

