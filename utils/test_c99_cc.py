
def test_C99_cc():
    if ("C99", 'cc') in invalid_lang_compilers:
        skip("`cc' command didn't work as expected (C99)")

