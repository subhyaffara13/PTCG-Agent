
def test_torf():
    v = [T, F, U]
    for i in product(*[v]*3):
        assert _torf(i) is (True if all(j for j in i) else
                            (False if all(j is False for j in i) else None))

