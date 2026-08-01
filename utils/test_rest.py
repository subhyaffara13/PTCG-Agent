
def test_rest():
    assert list(rest('ABCDE')) == list('BCDE')
    assert list(rest((3, 2, 1))) == list((2, 1))

