
def test_parsers_iso8601(date_str, exp):
    # see gh-12060
    #
    # Test only the ISO parser - flexibility to
    # different separators and leading zero's.
    actual = tslib._test_parse_iso8601(date_str)
    assert actual == exp

