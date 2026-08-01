
def test_altzeta():
    mp.dps = 15
    assert altzeta(-2) == 0
    assert altzeta(-4) == 0
    assert altzeta(-100) == 0
    assert altzeta(0) == 0.5
    assert altzeta(-1) == 0.25
    assert altzeta(-3) == -0.125
    assert altzeta(-5) == 0.25
    assert altzeta(-21) == 1180529130.25
    assert altzeta(1).ae(log(2))
    assert altzeta(2).ae(pi**2/12)
    assert altzeta(10).ae(73*pi**10/6842880)
    assert altzeta(50) < 1
    assert altzeta(60, rounding='d') < 1
    assert altzeta(60, rounding='u') == 1
    assert altzeta(10000, rounding='d') < 1
    assert altzeta(10000, rounding='u') == 1
    assert altzeta(3+0j) == altzeta(3)
    s = 3+4j
    assert altzeta(s).ae((1-2**(1-s))*zeta(s))
    s = -3+4j
    assert altzeta(s).ae((1-2**(1-s))*zeta(s))
    assert altzeta(-100.5).ae(4.58595480083585913e+108)
    assert altzeta(1.3).ae(0.73821404216623045)
    assert altzeta(1e-30).ae(0.5)
    assert altzeta(-1e-30).ae(0.5)
    assert altzeta(mpc(1e-30,1e-40)).ae(0.5)
    assert altzeta(mpc(-1e-30,1e-40)).ae(0.5)

