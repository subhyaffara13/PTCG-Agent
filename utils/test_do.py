
def test_do():
    inc = lambda x: x + 1
    assert do(inc, 1) == 1

    log = []
    assert do(log.append, 1) == 1
    assert log == [1]

