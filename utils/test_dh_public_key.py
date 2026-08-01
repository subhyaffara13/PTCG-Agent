
def test_dh_public_key():
    p1, g1, a = dh_private_key(digit = 100)
    p2, g2, ga = dh_public_key((p1, g1, a))
    assert p1 == p2
    assert g1 == g2
    assert ga == pow(g1, a, p1)

