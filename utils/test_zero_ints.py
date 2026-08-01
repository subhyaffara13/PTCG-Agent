
def test_zero_ints():
    expr = Basic(S(2), Basic(S(5), S(3)), S(8))
    expected = {Basic(S(0), Basic(S(0), S(0)), S(0))}

    brl = canon(posdec)
    assert set(brl(expr)) == expected

