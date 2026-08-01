
def test_unicode_names():
    assert parse_expr('α') == Symbol('α')

