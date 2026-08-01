
def test_rfc822_unescape(content, result):
    assert (result or content) == rfc822_unescape(rfc822_escape(content))

