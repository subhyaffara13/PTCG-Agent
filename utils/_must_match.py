
def _must_match(regex, string, pos):
    match = regex.match(string, pos)
    assert match is not None
    return match

