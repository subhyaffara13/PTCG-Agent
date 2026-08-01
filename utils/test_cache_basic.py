
def test_cache_basic():
    """ Test single symbol-like objects are cached when printed by themselves. """

    # Pairs of objects which should be considered equivalent with respect to caching
    pairs = [
        (x, sy.Symbol('x')),
        (X, sy.MatrixSymbol('X', *X.shape)),
        (f_t, sy.Function('f')(sy.Symbol('t'))),
    ]

    for s1, s2 in pairs:
        cache = {}
        st = aesara_code_(s1, cache=cache)

        # Test hit with same instance
        assert aesara_code_(s1, cache=cache) is st

        # Test miss with same instance but new cache
        assert aesara_code_(s1, cache={}) is not st

        # Test hit with different but equivalent instance
        assert aesara_code_(s2, cache=cache) is st


def test_cache_basic():
    """ Test single symbol-like objects are cached when printed by themselves. """

    # Pairs of objects which should be considered equivalent with respect to caching
    pairs = [
        (x, sy.Symbol('x')),
        (X, sy.MatrixSymbol('X', *X.shape)),
        (f_t, sy.Function('f')(sy.Symbol('t'))),
    ]

    for s1, s2 in pairs:
        cache = {}
        st = theano_code_(s1, cache=cache)

        # Test hit with same instance
        assert theano_code_(s1, cache=cache) is st

        # Test miss with same instance but new cache
        assert theano_code_(s1, cache={}) is not st

        # Test hit with different but equivalent instance
        assert theano_code_(s2, cache=cache) is st

