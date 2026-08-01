
def test_memoize_partial():
    def f(x, y=0):
        return x + y

    f2 = partial(f, y=1)
    fm2 = memoize(f2)

    assert fm2(3) == f2(3)
    assert fm2(3) == f2(3)

