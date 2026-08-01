
def _test_text_language(fig):
    t = fig.text(0, 0.8, 'Default', fontsize=32)
    assert t.get_language() is None
    t = fig.text(0, 0.55, 'Lang A', fontsize=32)
    assert t.get_language() is None
    t = fig.text(0, 0.3, 'Lang B', fontsize=32)
    assert t.get_language() is None
    t = fig.text(0, 0.05, 'Mixed', fontsize=32)
    assert t.get_language() is None

    # DejaVu Sans supports language-specific glyphs in the Serbian and Macedonian
    # languages in the Cyrillic alphabet.
    cyrillic = '\U00000431'
    t = fig.text(0.4, 0.8, cyrillic, fontsize=32)
    assert t.get_language() is None
    t = fig.text(0.4, 0.55, cyrillic, fontsize=32, language='sr')
    assert t.get_language() == 'sr'
    t = fig.text(0.4, 0.3, cyrillic, fontsize=32)
    t.set_language('ru')
    assert t.get_language() == 'ru'
    t = fig.text(0.4, 0.05, cyrillic * 4, fontsize=32,
                 language=[('ru', 0, 1), ('sr', 1, 2), ('ru', 2, 3), ('sr', 3, 4)])
    assert t.get_language() == (('ru', 0, 1), ('sr', 1, 2), ('ru', 2, 3), ('sr', 3, 4))

    # Or the Sámi family of languages in the Latin alphabet.
    latin = '\U0000014a'
    t = fig.text(0.7, 0.8, latin, fontsize=32)
    assert t.get_language() is None
    with plt.rc_context({'text.language': 'en'}):
        t = fig.text(0.7, 0.55, latin, fontsize=32)
    assert t.get_language() == 'en'
    t = fig.text(0.7, 0.3, latin, fontsize=32, language='smn')
    assert t.get_language() == 'smn'
    # Tuples are not documented, but we'll allow it.
    t = fig.text(0.7, 0.05, latin * 4, fontsize=32)
    t.set_language((('en', 0, 1), ('smn', 1, 2), ('en', 2, 3), ('smn', 3, 4)))
    assert t.get_language() == (
        ('en', 0, 1), ('smn', 1, 2), ('en', 2, 3), ('smn', 3, 4))

