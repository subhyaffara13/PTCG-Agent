
def test_hashable():
    '''
    test that interval objects are hashable.
    this is required in order to be able to put them into the cache, which
    appears to be necessary for plotting in py3k. For details, see:

    https://github.com/sympy/sympy/pull/2101
    https://github.com/sympy/sympy/issues/6533
    '''
    hash(interval(1, 1))
    hash(interval(1, 1, is_valid=True))
    hash(interval(-4, -0.5))
    hash(interval(-2, -0.5))
    hash(interval(0.25, 8.0))


def test_hashable():
    assert hash(NA) == hash(NA)
    d = {NA: "test"}
    assert d[NA] == "test"

