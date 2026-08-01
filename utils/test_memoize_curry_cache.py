
def test_memoize_curry_cache():
    @memoize(cache={1: True})
    def f(x):
        return False

    assert f(1) is True
    assert f(2) is False

