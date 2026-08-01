
def test_gamma_huge_7():
    mp.dps = 100
    a = 3 + j/mpf(10)**1000
    mp.dps = 15
    y = gamma(a)
    assert str(y.real) == "2.0"
    # wrong
    #assert str(y.imag) == "2.16735365342606e-1000"
    assert str(y.imag) == "1.84556867019693e-1000"
    mp.dps = 50
    y = gamma(a)
    assert str(y.real) == "2.0"
    #assert str(y.imag) == "2.1673536534260596065418805612488708028522563689298e-1000"
    assert str(y.imag) ==  "1.8455686701969342787869758198351951379156813281202e-1000"

