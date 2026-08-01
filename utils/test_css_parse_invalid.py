
def test_css_parse_invalid(invalid_css, remainder, msg):
    with tm.assert_produces_warning(CSSWarning, match=msg):
        assert_same_resolution(invalid_css, remainder)

