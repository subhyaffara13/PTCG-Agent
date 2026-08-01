
def test_pickle_to_tempfile():
    if not WINDOWS:  #see: https://bugs.python.org/issue14243
        dumpfile = dump(x)
        _x = load(dumpfile)
        assert _x == x

