
def test_top_down_once():
    top_rl = top_down_once(rl)

    assert top_rl(Basic(S(1.0), S(2.0), Basic(S(3), S(4)))) == \
        Basic2(S(1.0), S(2.0), Basic(S(3), S(4)))

