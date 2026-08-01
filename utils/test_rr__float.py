
def test_RR_Float():
    f1 = Float("1.01")
    f2 = Float("1.0000000000000000000001")
    assert f1._prec == 53
    assert f2._prec == 80
    assert RR(f1)-1 > 1e-50
    assert RR(f2)-1 < 1e-50 # RR's precision is lower than f2's

    RR2 = RealField(prec=f2._prec)
    assert RR2(f1)-1 > 1e-50
    assert RR2(f2)-1 > 1e-50 # RR's precision is equal to f2's

