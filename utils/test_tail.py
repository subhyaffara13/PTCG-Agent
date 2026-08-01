
def test_tail():
    assert list(tail(3, 'ABCDE')) == list('CDE')
    assert list(tail(3, iter('ABCDE'))) == list('CDE')
    assert list(tail(2, (3, 2, 1))) == list((2, 1))

