
def test_factor_cache():
    factor_cache.cache_clear()
    raises(ValueError, lambda: factor_cache.__setitem__(1, 5))
    raises(ValueError, lambda: factor_cache.__setitem__(10, 1))
    raises(ValueError, lambda: factor_cache.__setitem__(10, 10))
    raises(ValueError, lambda: factor_cache.__setitem__(10, 3))
    raises(ValueError, lambda: factor_cache.__setitem__(20, 4))
    factor_cache.maxsize = 3
    for i in range(2, 10):
        factor_cache[5*i] = 5
    assert len(factor_cache) == 3
    factor_cache.maxsize = 5
    for i in range(2, 10):
        factor_cache[5*i] = 5
    assert len(factor_cache) == 5
    factor_cache.maxsize = 2
    assert len(factor_cache) == 2
    factor_cache.maxsize =1000

    factor_cache.cache_clear()
    factor_cache[40] = 5
    assert factor_cache.get(40) == 5
    assert factor_cache.get(20) is None
    assert factor_cache[40] == 5
    raises(KeyError, lambda: factor_cache[10])
    del factor_cache[40]
    assert len(factor_cache) == 0
    raises(KeyError, lambda: factor_cache.__delitem__(40))
    factor_cache.add(100, [5, 2])
    assert len(factor_cache) == 2
    assert factor_cache[100] == 5

    for n in [1000000007, 10000019*20000003]:
        factorint(n)
        assert n in factor_cache

    # Restore the initial state
    factor_cache.cache_clear()
    factor_cache.maxsize = 1000

