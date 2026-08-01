
def test_exsqrt():
    assert ZZ.is_square(ZZ(4)) is True
    assert ZZ.exsqrt(ZZ(4)) == ZZ(2)
    assert ZZ.is_square(ZZ(42)) is False
    assert ZZ.exsqrt(ZZ(42)) is None
    assert ZZ.is_square(ZZ(0)) is True
    assert ZZ.exsqrt(ZZ(0)) == ZZ(0)
    assert ZZ.is_square(ZZ(-1)) is False
    assert ZZ.exsqrt(ZZ(-1)) is None

    assert QQ.is_square(QQ(9, 4)) is True
    assert QQ.exsqrt(QQ(9, 4)) == QQ(3, 2)
    assert QQ.is_square(QQ(18, 8)) is True
    assert QQ.exsqrt(QQ(18, 8)) == QQ(3, 2)
    assert QQ.is_square(QQ(-9, -4)) is True
    assert QQ.exsqrt(QQ(-9, -4)) == QQ(3, 2)
    assert QQ.is_square(QQ(11, 4)) is False
    assert QQ.exsqrt(QQ(11, 4)) is None
    assert QQ.is_square(QQ(9, 5)) is False
    assert QQ.exsqrt(QQ(9, 5)) is None
    assert QQ.is_square(QQ(4)) is True
    assert QQ.exsqrt(QQ(4)) == QQ(2)
    assert QQ.is_square(QQ(0)) is True
    assert QQ.exsqrt(QQ(0)) == QQ(0)
    assert QQ.is_square(QQ(-16, 9)) is False
    assert QQ.exsqrt(QQ(-16, 9)) is None

    assert RR.is_square(RR(6.25)) is True
    assert RR.exsqrt(RR(6.25)) == RR(2.5)
    assert RR.is_square(RR(2)) is True
    assert RR.almosteq(RR.exsqrt(RR(2)), RR(1.4142135623730951), tolerance=1e-15)
    assert RR.is_square(RR(0)) is True
    assert RR.exsqrt(RR(0)) == RR(0)
    assert RR.is_square(RR(-1)) is False
    assert RR.exsqrt(RR(-1)) is None

    assert CC.is_square(CC(2)) is True
    assert CC.almosteq(CC.exsqrt(CC(2)), CC(1.4142135623730951), tolerance=1e-15)
    assert CC.is_square(CC(0)) is True
    assert CC.exsqrt(CC(0)) == CC(0)
    assert CC.is_square(CC(-1)) is True
    assert CC.exsqrt(CC(-1)) == CC(0, 1)
    assert CC.is_square(CC(0, 2)) is True
    assert CC.exsqrt(CC(0, 2)) == CC(1, 1)
    assert CC.is_square(CC(-3, -4)) is True
    assert CC.exsqrt(CC(-3, -4)) == CC(1, -2)

    F2 = FF(2)
    assert F2.is_square(F2(1)) is True
    assert F2.exsqrt(F2(1)) == F2(1)
    assert F2.is_square(F2(0)) is True
    assert F2.exsqrt(F2(0)) == F2(0)

    F7 = FF(7)
    assert F7.is_square(F7(2)) is True
    assert F7.exsqrt(F7(2)) == F7(3)
    assert F7.is_square(F7(3)) is False
    assert F7.exsqrt(F7(3)) is None
    assert F7.is_square(F7(0)) is True
    assert F7.exsqrt(F7(0)) == F7(0)

