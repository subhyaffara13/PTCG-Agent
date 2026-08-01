
def test_trivial():
    assert findroot(lambda x: 0, 1) == 1
    assert findroot(lambda x: x, 0) == 0

