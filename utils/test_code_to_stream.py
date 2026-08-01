
def test_code_to_stream():
    pyfile = dumpIO_source(f, alias='_f')
    _f = loadIO_source(pyfile)
    assert _f(4) == f(4)

