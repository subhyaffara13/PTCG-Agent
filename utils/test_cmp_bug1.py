
def test_cmp_bug1():
    class T:
        pass

    t = T()
    x = Symbol("x")

    assert not (x == t)
    assert (x != t)

