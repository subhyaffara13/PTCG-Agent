
def test_concatv():
    assert list(concatv([], [], [])) == []
    assert (list(take(5, concatv(['a', 'b'], range(1000000000)))) ==
            ['a', 'b', 0, 1, 2])

