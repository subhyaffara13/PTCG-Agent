
def test_bottom_up_once():
    bottom_rl = bottom_up_once(rl)

    assert bottom_rl(Basic(S(1), S(2), Basic(S(3.0), S(4.0)))) == \
        Basic(S(1), S(2), Basic2(S(3.0), S(4.0)))

