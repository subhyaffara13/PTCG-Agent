
def test_can_set_locale_no_leak(lang, enc, lc_var):
    # Test that can_set_locale does not leak even when returning False. See GH#46595
    before_locale = _get_current_locale(lc_var)
    can_set_locale((lang, enc), locale.LC_ALL)
    after_locale = _get_current_locale(lc_var)
    assert before_locale == after_locale

