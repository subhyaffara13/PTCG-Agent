
def test_fourier():
    mp.dps = 15
    c, s = fourier(lambda x: x+1, [-1, 2], 2)
    #plot([lambda x: x+1, lambda x: fourierval((c, s), [-1, 2], x)], [-1, 2])
    assert c[0].ae(1.5)
    assert c[1].ae(-3*sqrt(3)/(2*pi))
    assert c[2].ae(3*sqrt(3)/(4*pi))
    assert s[0] == 0
    assert s[1].ae(3/(2*pi))
    assert s[2].ae(3/(4*pi))
    assert fourierval((c, s), [-1, 2], 1).ae(1.9134966715663442)

