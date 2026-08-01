
def test_igcdex():
    assert igcdex(2, 3) == (-1, 1, 1)
    assert igcdex(10, 12) == (-1, 1, 2)
    assert igcdex(100, 2004) == (-20, 1, 4)
    assert igcdex(0, 0) == (0, 0, 0)
    assert igcdex(1, 0) == (1, 0, 1)

