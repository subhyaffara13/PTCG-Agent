
def test_iroot():
    assert iroot(2, LONG_MAX) == (1, False)
    assert iroot(2, LONG_MAX + 1) == (1, False)
    for x in range(3):
        assert iroot(x, 1) == (x, True)
    raises(ValueError, lambda: iroot(-1, 1))
    raises(ValueError, lambda: iroot(0, 0))
    raises(ValueError, lambda: iroot(0, -1))

