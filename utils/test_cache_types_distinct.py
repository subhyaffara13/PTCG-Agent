
def test_cache_types_distinct():
    """
    Test that symbol-like objects of different types (Symbol, MatrixSymbol,
    AppliedUndef) are distinguished by the cache even if they have the same
    name.
    """
    symbols = [sy.Symbol('f_t'), sy.MatrixSymbol('f_t', 4, 4), f_t]

    cache = {}  # Single shared cache
    printed = {}

    for s in symbols:
        st = aesara_code_(s, cache=cache)
        assert st not in printed.values()
        printed[s] = st

    # Check all printed objects are distinct
    assert len(set(map(id, printed.values()))) == len(symbols)

    # Check retrieving
    for s, st in printed.items():
        with warns_deprecated_sympy():
            assert aesara_code(s, cache=cache) is st


def test_cache_types_distinct():
    """
    Test that symbol-like objects of different types (Symbol, MatrixSymbol,
    AppliedUndef) are distinguished by the cache even if they have the same
    name.
    """
    symbols = [sy.Symbol('f_t'), sy.MatrixSymbol('f_t', 4, 4), f_t]

    cache = {}  # Single shared cache
    printed = {}

    for s in symbols:
        st = theano_code_(s, cache=cache)
        assert st not in printed.values()
        printed[s] = st

    # Check all printed objects are distinct
    assert len(set(map(id, printed.values()))) == len(symbols)

    # Check retrieving
    for s, st in printed.items():
        with warns_deprecated_sympy():
            assert theano_code(s, cache=cache) is st

