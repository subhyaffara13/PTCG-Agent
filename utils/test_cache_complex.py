
def test_cache_complex():
    """
    Test caching on a complicated expression with multiple symbols appearing
    multiple times.
    """
    expr = x ** 2 + (y - sy.exp(x)) * sy.sin(z - x * y)
    symbol_names = {s.name for s in expr.free_symbols}
    expr_t = aesara_code_(expr)

    # Iterate through variables in the Aesara computational graph that the
    # printed expression depends on
    seen = set()
    for v in aesara.graph.basic.ancestors([expr_t]):
        # Owner-less, non-constant variables should be our symbols
        if v.owner is None and not isinstance(v, aesara.graph.basic.Constant):
            # Check it corresponds to a symbol and appears only once
            assert v.name in symbol_names
            assert v.name not in seen
            seen.add(v.name)

    # Check all were present
    assert seen == symbol_names


def test_cache_complex():
    """
    Test caching on a complicated expression with multiple symbols appearing
    multiple times.
    """
    expr = x ** 2 + (y - sy.exp(x)) * sy.sin(z - x * y)
    symbol_names = {s.name for s in expr.free_symbols}
    expr_t = theano_code_(expr)

    # Iterate through variables in the Theano computational graph that the
    # printed expression depends on
    seen = set()
    for v in theano.gof.graph.ancestors([expr_t]):
        # Owner-less, non-constant variables should be our symbols
        if v.owner is None and not isinstance(v, theano.gof.graph.Constant):
            # Check it corresponds to a symbol and appears only once
            assert v.name in symbol_names
            assert v.name not in seen
            seen.add(v.name)

    # Check all were present
    assert seen == symbol_names

