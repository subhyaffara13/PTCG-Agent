
def test_fac2():
    mp.dps = 15
    assert [fac2(n) for n in range(10)] == [1,1,2,3,8,15,48,105,384,945]
    assert fac2(-5).ae(1./3)
    assert fac2(-11).ae(-1./945)
    assert fac2(50).ae(5.20469842636666623e32)
    assert fac2(0.5+0.75j).ae(0.81546769394688069176-0.34901016085573266889j)
    assert fac2(inf) == inf
    assert isnan(fac2(-inf))

