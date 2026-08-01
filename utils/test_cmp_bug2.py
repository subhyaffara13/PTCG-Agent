
def test_cmp_bug2():
    class T:
        pass

    t = T()

    assert not (Symbol == t)
    assert (Symbol != t)

