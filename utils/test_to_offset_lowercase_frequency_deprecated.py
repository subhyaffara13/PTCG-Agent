
def test_to_offset_lowercase_frequency_deprecated(freq_depr, expected):
    # GH#54939, GH#58998
    msg = f"'{freq_depr[1:]}' is deprecated and will be removed in a future version."

    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        result = to_offset(freq_depr)
    assert result == expected

