
def test_ANP_unify():
    mod_z = [ZZ(1), ZZ(0), ZZ(-2)]
    mod_q = [QQ(1), QQ(0), QQ(-2)]

    a = ANP([QQ(1)], mod_q, QQ)
    b = ANP([ZZ(1)], mod_z, ZZ)

    assert a.unify(b)[0] == QQ
    assert b.unify(a)[0] == QQ
    assert a.unify(a)[0] == QQ
    assert b.unify(b)[0] == ZZ

    assert a.unify_ANP(b)[-1] == QQ
    assert b.unify_ANP(a)[-1] == QQ
    assert a.unify_ANP(a)[-1] == QQ
    assert b.unify_ANP(b)[-1] == ZZ

