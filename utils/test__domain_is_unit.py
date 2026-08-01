
def test_Domain_is_unit():
    nums = [-2, -1, 0, 1, 2]
    invring = [False, True, False, True, False]
    invfield = [True, True, False, True, True]
    ZZx, QQx, QQxf = ZZ[x], QQ[x], QQ.frac_field(x)
    assert [ZZ.is_unit(ZZ(n)) for n in nums] == invring
    assert [QQ.is_unit(QQ(n)) for n in nums] == invfield
    assert [ZZx.is_unit(ZZx(n)) for n in nums] == invring
    assert [QQx.is_unit(QQx(n)) for n in nums] == invfield
    assert [QQxf.is_unit(QQxf(n)) for n in nums] == invfield
    assert ZZx.is_unit(ZZx(x)) is False
    assert QQx.is_unit(QQx(x)) is False
    assert QQxf.is_unit(QQxf(x)) is True

