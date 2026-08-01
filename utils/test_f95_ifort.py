
def test_F95_ifort():
    if ("F95", 'ifort') in invalid_lang_compilers:
        skip("`ifort' command didn't work as expected")

