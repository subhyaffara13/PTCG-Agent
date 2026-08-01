
def test_pickle_to_stream():
    dumpfile = dumpIO(x)
    _x = loadIO(dumpfile)
    assert _x == x

