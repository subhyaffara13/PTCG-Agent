
def test_C89_cc():
    if ("C89", 'cc') in invalid_lang_compilers:
        skip("`cc' command didn't work as expected (C89)")

