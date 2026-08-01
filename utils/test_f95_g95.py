
def test_F95_g95():
    if ("F95", 'g95') in invalid_lang_compilers:
        skip("`g95' command didn't work as expected")

