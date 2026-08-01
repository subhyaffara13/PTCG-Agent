
def test_exp_hp():
    mp.dps = 4000
    r = exp(mpf(1)/10)
    # IntegerPart[N[Exp[1/10] * 10^4000, 4000]]
    # ...92167105162069688129
    assert int(r * 10**mp.dps) % 10**20 == 92167105162069688129

