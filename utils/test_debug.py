
def test_debug():
    file = StringIO()
    rl = debug(posdec, file)
    rl(5)
    log = file.getvalue()
    file.close()

    assert posdec.__name__ in log
    assert '5' in log
    assert '4' in log


def test_debug():
    from io import StringIO
    file = StringIO()
    rl = debug(posdec, file)
    list(rl(5))
    log = file.getvalue()
    file.close()

    assert posdec.__name__ in log
    assert '5' in log
    assert '4' in log

