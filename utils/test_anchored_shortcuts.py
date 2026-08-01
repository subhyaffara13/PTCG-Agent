
def test_anchored_shortcuts(shortcut, expected):
    result = to_offset(shortcut)
    assert result == expected

