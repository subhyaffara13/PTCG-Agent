
def test_gcd_hypothesis(f, g, r):
    gcd_1 = f.gcd(g)
    gcd_2 = g.gcd(f)
    assert gcd_1 == gcd_2

    # multiply by r
    gcd_3 = g.gcd(f + r * g)
    assert gcd_1 == gcd_3

