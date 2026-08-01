
def test_pure_key_dict():
    p = D()
    assert (x in p) is False
    assert (1 in p) is False
    p[x] = 1
    assert x in p
    assert y in p
    assert p[y] == 1
    raises(KeyError, lambda: p[1])
    def dont(k):
        p[k] = 2
    raises(ValueError, lambda: dont(1))

