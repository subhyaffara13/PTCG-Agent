
def test_Domain___eq__():
    assert (ZZ[x, y] == ZZ[x, y]) is True
    assert (QQ[x, y] == QQ[x, y]) is True

    assert (ZZ[x, y] == QQ[x, y]) is False
    assert (QQ[x, y] == ZZ[x, y]) is False

    assert (ZZ.frac_field(x, y) == ZZ.frac_field(x, y)) is True
    assert (QQ.frac_field(x, y) == QQ.frac_field(x, y)) is True

    assert (ZZ.frac_field(x, y) == QQ.frac_field(x, y)) is False
    assert (QQ.frac_field(x, y) == ZZ.frac_field(x, y)) is False

    assert RealField()[x] == RR[x]

