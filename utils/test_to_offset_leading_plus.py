
def test_to_offset_leading_plus(freqstr, expected, wrn):
    msg = "'d' is deprecated and will be removed in a future version."

    with tm.assert_produces_warning(wrn, match=msg):
        result = to_offset(freqstr)
    assert result.n == expected

