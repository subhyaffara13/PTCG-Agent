
def test_Domain_unify():
    F3 = GF(3)
    F5 = GF(5)

    assert unify(F3, F3) == F3
    raises(UnificationFailed, lambda: unify(F3, ZZ))
    raises(UnificationFailed, lambda: unify(F3, QQ))
    raises(UnificationFailed, lambda: unify(F3, ZZ_I))
    raises(UnificationFailed, lambda: unify(F3, QQ_I))
    raises(UnificationFailed, lambda: unify(F3, ALG))
    raises(UnificationFailed, lambda: unify(F3, RR))
    raises(UnificationFailed, lambda: unify(F3, CC))
    raises(UnificationFailed, lambda: unify(F3, ZZ[x]))
    raises(UnificationFailed, lambda: unify(F3, ZZ.frac_field(x)))
    raises(UnificationFailed, lambda: unify(F3, EX))

    assert unify(F5, F5) == F5
    raises(UnificationFailed, lambda: unify(F5, F3))
    raises(UnificationFailed, lambda: unify(F5, F3[x]))
    raises(UnificationFailed, lambda: unify(F5, F3.frac_field(x)))

    raises(UnificationFailed, lambda: unify(ZZ, F3))
    assert unify(ZZ, ZZ) == ZZ
    assert unify(ZZ, QQ) == QQ
    assert unify(ZZ, ALG) == ALG
    assert unify(ZZ, RR) == RR
    assert unify(ZZ, CC) == CC
    assert unify(ZZ, ZZ[x]) == ZZ[x]
    assert unify(ZZ, ZZ.frac_field(x)) == ZZ.frac_field(x)
    assert unify(ZZ, EX) == EX

    raises(UnificationFailed, lambda: unify(QQ, F3))
    assert unify(QQ, ZZ) == QQ
    assert unify(QQ, QQ) == QQ
    assert unify(QQ, ALG) == ALG
    assert unify(QQ, RR) == RR
    assert unify(QQ, CC) == CC
    assert unify(QQ, ZZ[x]) == QQ[x]
    assert unify(QQ, ZZ.frac_field(x)) == QQ.frac_field(x)
    assert unify(QQ, EX) == EX

    raises(UnificationFailed, lambda: unify(ZZ_I, F3))
    assert unify(ZZ_I, ZZ) == ZZ_I
    assert unify(ZZ_I, ZZ_I) == ZZ_I
    assert unify(ZZ_I, QQ) == QQ_I
    assert unify(ZZ_I, ALG) == QQ.algebraic_field(I, sqrt(2), sqrt(3))
    assert unify(ZZ_I, RR) == CC
    assert unify(ZZ_I, CC) == CC
    assert unify(ZZ_I, ZZ[x]) == ZZ_I[x]
    assert unify(ZZ_I, ZZ_I[x]) == ZZ_I[x]
    assert unify(ZZ_I, ZZ.frac_field(x)) == ZZ_I.frac_field(x)
    assert unify(ZZ_I, ZZ_I.frac_field(x)) == ZZ_I.frac_field(x)
    assert unify(ZZ_I, EX) == EX

    raises(UnificationFailed, lambda: unify(QQ_I, F3))
    assert unify(QQ_I, ZZ) == QQ_I
    assert unify(QQ_I, ZZ_I) == QQ_I
    assert unify(QQ_I, QQ) == QQ_I
    assert unify(QQ_I, ALG) == QQ.algebraic_field(I, sqrt(2), sqrt(3))
    assert unify(QQ_I, RR) == CC
    assert unify(QQ_I, CC) == CC
    assert unify(QQ_I, ZZ[x]) == QQ_I[x]
    assert unify(QQ_I, ZZ_I[x]) == QQ_I[x]
    assert unify(QQ_I, QQ[x]) == QQ_I[x]
    assert unify(QQ_I, QQ_I[x]) == QQ_I[x]
    assert unify(QQ_I, ZZ.frac_field(x)) == QQ_I.frac_field(x)
    assert unify(QQ_I, ZZ_I.frac_field(x)) == QQ_I.frac_field(x)
    assert unify(QQ_I, QQ.frac_field(x)) == QQ_I.frac_field(x)
    assert unify(QQ_I, QQ_I.frac_field(x)) == QQ_I.frac_field(x)
    assert unify(QQ_I, EX) == EX

    raises(UnificationFailed, lambda: unify(RR, F3))
    assert unify(RR, ZZ) == RR
    assert unify(RR, QQ) == RR
    assert unify(RR, ALG) == RR
    assert unify(RR, RR) == RR
    assert unify(RR, CC) == CC
    assert unify(RR, ZZ[x]) == RR[x]
    assert unify(RR, ZZ.frac_field(x)) == RR.frac_field(x)
    assert unify(RR, EX) == EX
    assert RR[x].unify(ZZ.frac_field(y)) == RR.frac_field(x, y)

    raises(UnificationFailed, lambda: unify(CC, F3))
    assert unify(CC, ZZ) == CC
    assert unify(CC, QQ) == CC
    assert unify(CC, ALG) == CC
    assert unify(CC, RR) == CC
    assert unify(CC, CC) == CC
    assert unify(CC, ZZ[x]) == CC[x]
    assert unify(CC, ZZ.frac_field(x)) == CC.frac_field(x)
    assert unify(CC, EX) == EX

    raises(UnificationFailed, lambda: unify(ZZ[x], F3))
    assert unify(ZZ[x], ZZ) == ZZ[x]
    assert unify(ZZ[x], QQ) == QQ[x]
    assert unify(ZZ[x], ALG) == ALG[x]
    assert unify(ZZ[x], RR) == RR[x]
    assert unify(ZZ[x], CC) == CC[x]
    assert unify(ZZ[x], ZZ[x]) == ZZ[x]
    assert unify(ZZ[x], ZZ.frac_field(x)) == ZZ.frac_field(x)
    assert unify(ZZ[x], EX) == EX

    raises(UnificationFailed, lambda: unify(ZZ.frac_field(x), F3))
    assert unify(ZZ.frac_field(x), ZZ) == ZZ.frac_field(x)
    assert unify(ZZ.frac_field(x), QQ) == QQ.frac_field(x)
    assert unify(ZZ.frac_field(x), ALG) == ALG.frac_field(x)
    assert unify(ZZ.frac_field(x), RR) == RR.frac_field(x)
    assert unify(ZZ.frac_field(x), CC) == CC.frac_field(x)
    assert unify(ZZ.frac_field(x), ZZ[x]) == ZZ.frac_field(x)
    assert unify(ZZ.frac_field(x), ZZ.frac_field(x)) == ZZ.frac_field(x)
    assert unify(ZZ.frac_field(x), EX) == EX

    raises(UnificationFailed, lambda: unify(EX, F3))
    assert unify(EX, ZZ) == EX
    assert unify(EX, QQ) == EX
    assert unify(EX, ALG) == EX
    assert unify(EX, RR) == EX
    assert unify(EX, CC) == EX
    assert unify(EX, ZZ[x]) == EX
    assert unify(EX, ZZ.frac_field(x)) == EX
    assert unify(EX, EX) == EX

