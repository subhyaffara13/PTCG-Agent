
def test_F95_gfortran():
    if ("F95", 'gfortran') in invalid_lang_compilers:
        skip("`gfortran' command didn't work as expected")

