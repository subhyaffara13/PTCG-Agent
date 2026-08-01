
def test_get_locales_prefix():
    first_locale = _all_locales[0]
    assert len(get_locales(prefix=first_locale[:2])) > 0

