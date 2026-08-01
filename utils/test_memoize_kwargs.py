
def test_memoize_kwargs():
    fn_calls = [0]  # Storage for side effects

    def f(x, y=0):
        return x + y

    mf = memoize(f)

    assert mf(1) == f(1)
    assert mf(1, 2) == f(1, 2)
    assert mf(1, y=2) == f(1, y=2)
    assert mf(1, y=3) == f(1, y=3)

