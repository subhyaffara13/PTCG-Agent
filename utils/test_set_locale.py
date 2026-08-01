
def test_set_locale(lang, enc):
    before_locale = _get_current_locale()

    enc = codecs.lookup(enc).name
    new_locale = lang, enc

    if not can_set_locale(new_locale):
        msg = "unsupported locale setting"

        with pytest.raises(locale.Error, match=msg):
            with set_locale(new_locale):
                pass
    else:
        with set_locale(new_locale) as normalized_locale:
            new_lang, new_enc = normalized_locale.split(".")
            new_enc = codecs.lookup(enc).name

            normalized_locale = new_lang, new_enc
            assert normalized_locale == new_locale

    # Once we exit the "with" statement, locale should be back to what it was.
    after_locale = _get_current_locale()
    assert before_locale == after_locale

