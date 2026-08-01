
def test_sall():
    zero_onelevel = sall(zero_symbols)

    assert zero_onelevel(Basic(x, y, Basic(x, z))) == \
        Basic(S(0), S(0), Basic(x, z))


def test_sall():
    expr = Basic(S(1), S(2))
    expected = Basic(S(2), S(3))
    brl = sall(inc)

    assert list(brl(expr)) == [expected]

    expr = Basic(S(1), S(2), Basic(S(3), S(4)))
    expected = Basic(S(2), S(3), Basic(S(3), S(4)))
    brl = sall(do_one(inc, identity))

    assert list(brl(expr)) == [expected]

