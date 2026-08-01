
def test_code_to_tempfile():
    if not WINDOWS:  #see: https://bugs.python.org/issue14243
        pyfile = dump_source(f, alias='_f')
        _f = load_source(pyfile)
        assert _f(4) == f(4)

