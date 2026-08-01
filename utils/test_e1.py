
def test_e1():
    mp.dps = 15
    assert e1(0) == inf
    assert e1(inf) == 0
    assert e1(-inf) == mpc(-inf, -pi)
    assert e1(10j).ae(0.045456433004455372635 + 0.087551267423977430100j)
    assert e1(100j).ae(0.0051488251426104921444 - 0.0085708599058403258790j)
    assert e1(fmul(10**20, j, exact=True)).ae(6.4525128526578084421e-21 - 7.6397040444172830039e-21j, abs_eps=0, rel_eps=8*eps)
    assert e1(-10j).ae(0.045456433004455372635 - 0.087551267423977430100j)
    assert e1(-100j).ae(0.0051488251426104921444 + 0.0085708599058403258790j)
    assert e1(fmul(-10**20, j, exact=True)).ae(6.4525128526578084421e-21 + 7.6397040444172830039e-21j, abs_eps=0, rel_eps=8*eps)

