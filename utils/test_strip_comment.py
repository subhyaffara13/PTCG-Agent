
def test_strip_comment(line, result):
    """Strip everything from the first unquoted #."""
    assert cbook._strip_comment(line) == result

