
def test_top_down_big_tree():
    expr = Basic(S(1), Basic(S(2)), Basic(S(3), Basic(S(4)), S(5)))
    expected = Basic(S(2), Basic(S(3)), Basic(S(4), Basic(S(5)), S(6)))
    brl = top_down(inc)

    assert set(brl(expr)) == {expected}

