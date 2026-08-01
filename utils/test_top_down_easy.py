
def test_top_down_easy():
    expr = Basic(S(1), S(2))
    expected = Basic(S(2), S(3))
    brl = top_down(inc)

    assert set(brl(expr)) == {expected}

