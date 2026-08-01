
def test_Poly__unify():
    raises(UnificationFailed, lambda: Poly(x)._unify(y))

    F3 = FF(3)

    assert Poly(x, x, modulus=3)._unify(Poly(y, y, modulus=3))[2:] == (
        DMP([[F3(1)], []], F3), DMP([[F3(1), F3(0)]], F3))
    raises(UnificationFailed, lambda: Poly(x, x, modulus=3)._unify(Poly(y, y, modulus=5)))

    raises(UnificationFailed, lambda: Poly(y, x, y)._unify(Poly(x, x, modulus=3)))
    raises(UnificationFailed, lambda: Poly(x, x, modulus=3)._unify(Poly(y, x, y)))

    assert Poly(x + 1, x)._unify(Poly(x + 2, x))[2:] ==\
        (DMP([ZZ(1), ZZ(1)], ZZ), DMP([ZZ(1), ZZ(2)], ZZ))
    assert Poly(x + 1, x, domain='QQ')._unify(Poly(x + 2, x))[2:] ==\
        (DMP([QQ(1), QQ(1)], QQ), DMP([QQ(1), QQ(2)], QQ))
    assert Poly(x + 1, x)._unify(Poly(x + 2, x, domain='QQ'))[2:] ==\
        (DMP([QQ(1), QQ(1)], QQ), DMP([QQ(1), QQ(2)], QQ))

    assert Poly(x + 1, x)._unify(Poly(x + 2, x, y))[2:] ==\
        (DMP([[ZZ(1)], [ZZ(1)]], ZZ), DMP([[ZZ(1)], [ZZ(2)]], ZZ))
    assert Poly(x + 1, x, domain='QQ')._unify(Poly(x + 2, x, y))[2:] ==\
        (DMP([[QQ(1)], [QQ(1)]], QQ), DMP([[QQ(1)], [QQ(2)]], QQ))
    assert Poly(x + 1, x)._unify(Poly(x + 2, x, y, domain='QQ'))[2:] ==\
        (DMP([[QQ(1)], [QQ(1)]], QQ), DMP([[QQ(1)], [QQ(2)]], QQ))

    assert Poly(x + 1, x, y)._unify(Poly(x + 2, x))[2:] ==\
        (DMP([[ZZ(1)], [ZZ(1)]], ZZ), DMP([[ZZ(1)], [ZZ(2)]], ZZ))
    assert Poly(x + 1, x, y, domain='QQ')._unify(Poly(x + 2, x))[2:] ==\
        (DMP([[QQ(1)], [QQ(1)]], QQ), DMP([[QQ(1)], [QQ(2)]], QQ))
    assert Poly(x + 1, x, y)._unify(Poly(x + 2, x, domain='QQ'))[2:] ==\
        (DMP([[QQ(1)], [QQ(1)]], QQ), DMP([[QQ(1)], [QQ(2)]], QQ))

    assert Poly(x + 1, x, y)._unify(Poly(x + 2, x, y))[2:] ==\
        (DMP([[ZZ(1)], [ZZ(1)]], ZZ), DMP([[ZZ(1)], [ZZ(2)]], ZZ))
    assert Poly(x + 1, x, y, domain='QQ')._unify(Poly(x + 2, x, y))[2:] ==\
        (DMP([[QQ(1)], [QQ(1)]], QQ), DMP([[QQ(1)], [QQ(2)]], QQ))
    assert Poly(x + 1, x, y)._unify(Poly(x + 2, x, y, domain='QQ'))[2:] ==\
        (DMP([[QQ(1)], [QQ(1)]], QQ), DMP([[QQ(1)], [QQ(2)]], QQ))

    assert Poly(x + 1, x)._unify(Poly(x + 2, y, x))[2:] ==\
        (DMP([[ZZ(1), ZZ(1)]], ZZ), DMP([[ZZ(1), ZZ(2)]], ZZ))
    assert Poly(x + 1, x, domain='QQ')._unify(Poly(x + 2, y, x))[2:] ==\
        (DMP([[QQ(1), QQ(1)]], QQ), DMP([[QQ(1), QQ(2)]], QQ))
    assert Poly(x + 1, x)._unify(Poly(x + 2, y, x, domain='QQ'))[2:] ==\
        (DMP([[QQ(1), QQ(1)]], QQ), DMP([[QQ(1), QQ(2)]], QQ))

    assert Poly(x + 1, y, x)._unify(Poly(x + 2, x))[2:] ==\
        (DMP([[ZZ(1), ZZ(1)]], ZZ), DMP([[ZZ(1), ZZ(2)]], ZZ))
    assert Poly(x + 1, y, x, domain='QQ')._unify(Poly(x + 2, x))[2:] ==\
        (DMP([[QQ(1), QQ(1)]], QQ), DMP([[QQ(1), QQ(2)]], QQ))
    assert Poly(x + 1, y, x)._unify(Poly(x + 2, x, domain='QQ'))[2:] ==\
        (DMP([[QQ(1), QQ(1)]], QQ), DMP([[QQ(1), QQ(2)]], QQ))

    assert Poly(x + 1, x, y)._unify(Poly(x + 2, y, x))[2:] ==\
        (DMP([[ZZ(1)], [ZZ(1)]], ZZ), DMP([[ZZ(1)], [ZZ(2)]], ZZ))
    assert Poly(x + 1, x, y, domain='QQ')._unify(Poly(x + 2, y, x))[2:] ==\
        (DMP([[QQ(1)], [QQ(1)]], QQ), DMP([[QQ(1)], [QQ(2)]], QQ))
    assert Poly(x + 1, x, y)._unify(Poly(x + 2, y, x, domain='QQ'))[2:] ==\
        (DMP([[QQ(1)], [QQ(1)]], QQ), DMP([[QQ(1)], [QQ(2)]], QQ))

    assert Poly(x + 1, y, x)._unify(Poly(x + 2, x, y))[2:] ==\
        (DMP([[ZZ(1), ZZ(1)]], ZZ), DMP([[ZZ(1), ZZ(2)]], ZZ))
    assert Poly(x + 1, y, x, domain='QQ')._unify(Poly(x + 2, x, y))[2:] ==\
        (DMP([[QQ(1), QQ(1)]], QQ), DMP([[QQ(1), QQ(2)]], QQ))
    assert Poly(x + 1, y, x)._unify(Poly(x + 2, x, y, domain='QQ'))[2:] ==\
        (DMP([[QQ(1), QQ(1)]], QQ), DMP([[QQ(1), QQ(2)]], QQ))

    assert Poly(x**2 + I, x, domain=ZZ_I).unify(Poly(x**2 + sqrt(2), x, extension=True)) == \
            (Poly(x**2 + I, x, domain='QQ<sqrt(2) + I>'), Poly(x**2 + sqrt(2), x, domain='QQ<sqrt(2) + I>'))

    F, A, B = field("a,b", ZZ)

    assert Poly(a*x, x, domain='ZZ[a]')._unify(Poly(a*b*x, x, domain='ZZ(a,b)'))[2:] == \
        (DMP([A, F(0)], F.to_domain()), DMP([A*B, F(0)], F.to_domain()))

    assert Poly(a*x, x, domain='ZZ(a)')._unify(Poly(a*b*x, x, domain='ZZ(a,b)'))[2:] == \
        (DMP([A, F(0)], F.to_domain()), DMP([A*B, F(0)], F.to_domain()))

    raises(CoercionFailed, lambda: Poly(Poly(x**2 + x**2*z, y, field=True), domain='ZZ(x)'))

    f = Poly(t**2 + t/3 + x, t, domain='QQ(x)')
    g = Poly(t**2 + t/3 + x, t, domain='QQ[x]')

    assert f._unify(g)[2:] == (f.rep, f.rep)

