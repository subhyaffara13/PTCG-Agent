
def test_complicated_symbol_unchanged():
    for symb_name in ["dexpr2_d1tau", "dexpr2^d1tau"]:
        assert pretty(Symbol(symb_name)) == symb_name

