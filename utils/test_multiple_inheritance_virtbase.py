
def test_multiple_inheritance_virtbase():
    class MITypePy(m.Base12a):
        def __init__(self, i, j):
            m.Base12a.__init__(self, i, j)

    mt = MITypePy(3, 4)
    assert mt.bar() == 4
    assert m.bar_base2a(mt) == 4
    assert m.bar_base2a_sharedptr(mt) == 4

