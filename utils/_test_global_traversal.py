
def _test_global_traversal(trav):
    zero_all_symbols = trav(zero_symbols)

    assert zero_all_symbols(Basic(x, y, Basic(x, z))) == \
        Basic(S(0), S(0), Basic(S(0), S(0)))

