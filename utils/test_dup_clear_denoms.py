
def test_dup_clear_denoms():
    assert dup_clear_denoms([], QQ, ZZ) == (ZZ(1), [])

    assert dup_clear_denoms([QQ(1)], QQ, ZZ) == (ZZ(1), [QQ(1)])
    assert dup_clear_denoms([QQ(7)], QQ, ZZ) == (ZZ(1), [QQ(7)])

    assert dup_clear_denoms([QQ(7, 3)], QQ) == (ZZ(3), [QQ(7)])
    assert dup_clear_denoms([QQ(7, 3)], QQ, ZZ) == (ZZ(3), [QQ(7)])

    assert dup_clear_denoms(
        [QQ(3), QQ(1), QQ(0)], QQ, ZZ) == (ZZ(1), [QQ(3), QQ(1), QQ(0)])
    assert dup_clear_denoms(
        [QQ(1), QQ(1, 2), QQ(0)], QQ, ZZ) == (ZZ(2), [QQ(2), QQ(1), QQ(0)])

    assert dup_clear_denoms([QQ(3), QQ(
        1), QQ(0)], QQ, ZZ, convert=True) == (ZZ(1), [ZZ(3), ZZ(1), ZZ(0)])
    assert dup_clear_denoms([QQ(1), QQ(
        1, 2), QQ(0)], QQ, ZZ, convert=True) == (ZZ(2), [ZZ(2), ZZ(1), ZZ(0)])

    assert dup_clear_denoms(
        [EX(S(3)/2), EX(S(9)/4)], EX) == (EX(4), [EX(6), EX(9)])

    assert dup_clear_denoms([EX(7)], EX) == (EX(1), [EX(7)])
    assert dup_clear_denoms([EX(sin(x)/x), EX(0)], EX) == (EX(x), [EX(sin(x)), EX(0)])

    F = RR.frac_field(x)
    result = dup_clear_denoms([F(8.48717/(8.0089*x + 2.83)), F(0.0)], F)
    assert str(result) == "(x + 0.353356890459364, [1.05971731448763, 0.0])"

