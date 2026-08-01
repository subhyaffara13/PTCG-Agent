
def test_to_offset_uppercase_frequency_deprecated(freq_depr):
    # GH#54939
    depr_msg = (
        f"'{freq_depr[1:]}' is deprecated and will be removed in a "
        f"future version, please use '{freq_depr.lower()[1:]}' instead."
    )

    with tm.assert_produces_warning(Pandas4Warning, match=depr_msg):
        to_offset(freq_depr)

