
def test_zeta_huge():
    mp.dps = 15
    assert zeta(inf) == 1
    mp.dps = 50
    assert zeta(100).ae('1.0000000000000000000000000000007888609052210118073522')
    assert zeta(40*pi).ae('1.0000000000000000000000000000000000000148407238666182')
    mp.dps = 10000
    v = zeta(33000)
    mp.dps = 15
    assert str(v-1) == '1.02363019598118e-9934'
    assert zeta(pi*1000, rounding=round_up) > 1
    assert zeta(3000, rounding=round_up) > 1
    assert zeta(pi*1000) == 1
    assert zeta(3000) == 1

