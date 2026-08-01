
def test_zeta():
    s = S(5)
    x = Zeta('x', s)
    assert E(x) == zeta(s-1) / zeta(s)
    assert simplify(variance(x)) == (
        zeta(s) * zeta(s-2) - zeta(s-1)**2) / zeta(s)**2


def test_zeta():
    assert str(zeta(3)) == "zeta(3)"


def test_zeta():
    assert_allclose(sc.zeta(2,2), np.pi**2/6 - 1, rtol=1e-12)


def test_zeta():
    mp.dps = 15
    assert zeta(2).ae(pi**2 / 6)
    assert zeta(2.0).ae(pi**2 / 6)
    assert zeta(mpc(2)).ae(pi**2 / 6)
    assert zeta(100).ae(1)
    assert zeta(0).ae(-0.5)
    assert zeta(0.5).ae(-1.46035450880958681)
    assert zeta(-1).ae(-mpf(1)/12)
    assert zeta(-2) == 0
    assert zeta(-3).ae(mpf(1)/120)
    assert zeta(-4) == 0
    assert zeta(-100) == 0
    assert isnan(zeta(nan))
    assert zeta(1e-30).ae(-0.5)
    assert zeta(-1e-30).ae(-0.5)
    # Zeros in the critical strip
    assert zeta(mpc(0.5, 14.1347251417346937904)).ae(0)
    assert zeta(mpc(0.5, 21.0220396387715549926)).ae(0)
    assert zeta(mpc(0.5, 25.0108575801456887632)).ae(0)
    assert zeta(mpc(1e-30,1e-40)).ae(-0.5)
    assert zeta(mpc(-1e-30,1e-40)).ae(-0.5)
    mp.dps = 50
    im = '236.5242296658162058024755079556629786895294952121891237'
    assert zeta(mpc(0.5, im)).ae(0, 1e-46)
    mp.dps = 15
    # Complex reflection formula
    assert (zeta(-60+3j) / 10**34).ae(8.6270183987866146+15.337398548226238j)
    # issue #358
    assert zeta(0,0.5) == 0
    assert zeta(0,0) == 0.5
    assert zeta(0,0.5,1).ae(-0.34657359027997265)
    # see issue #390
    assert zeta(-1.5,0.5j).ae(-0.13671400162512768475 + 0.11411333638426559139j)

