
def test_arity():
    f = lambda x, y: 1
    assert arity(f) == 2
    def f(x, y, z=None):
        pass
    assert arity(f) == (2, 3)
    assert arity(lambda *x: x) is None
    assert arity(log) == (1, 2)

