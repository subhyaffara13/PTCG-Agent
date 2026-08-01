
def test_Domain_unify_FiniteExtension():
    KxZZ = FiniteExtension(Poly(x**2 - 2, x, domain=ZZ))
    KxQQ = FiniteExtension(Poly(x**2 - 2, x, domain=QQ))
    KxZZy = FiniteExtension(Poly(x**2 - 2, x, domain=ZZ[y]))
    KxQQy = FiniteExtension(Poly(x**2 - 2, x, domain=QQ[y]))

    assert KxZZ.unify(KxZZ) == KxZZ
    assert KxQQ.unify(KxQQ) == KxQQ
    assert KxZZy.unify(KxZZy) == KxZZy
    assert KxQQy.unify(KxQQy) == KxQQy

    assert KxZZ.unify(ZZ) == KxZZ
    assert KxZZ.unify(QQ) == KxQQ
    assert KxQQ.unify(ZZ) == KxQQ
    assert KxQQ.unify(QQ) == KxQQ

    assert KxZZ.unify(ZZ[y]) == KxZZy
    assert KxZZ.unify(QQ[y]) == KxQQy
    assert KxQQ.unify(ZZ[y]) == KxQQy
    assert KxQQ.unify(QQ[y]) == KxQQy

    assert KxZZy.unify(ZZ) == KxZZy
    assert KxZZy.unify(QQ) == KxQQy
    assert KxQQy.unify(ZZ) == KxQQy
    assert KxQQy.unify(QQ) == KxQQy

    assert KxZZy.unify(ZZ[y]) == KxZZy
    assert KxZZy.unify(QQ[y]) == KxQQy
    assert KxQQy.unify(ZZ[y]) == KxQQy
    assert KxQQy.unify(QQ[y]) == KxQQy

    K = FiniteExtension(Poly(x**2 - 2, x, domain=ZZ[y]))
    assert K.unify(ZZ) == K
    assert K.unify(ZZ[x]) == K
    assert K.unify(ZZ[y]) == K
    assert K.unify(ZZ[x, y]) == K

    Kz = FiniteExtension(Poly(x**2 - 2, x, domain=ZZ[y, z]))
    assert K.unify(ZZ[z]) == Kz
    assert K.unify(ZZ[x, z]) == Kz
    assert K.unify(ZZ[y, z]) == Kz
    assert K.unify(ZZ[x, y, z]) == Kz

    Kx = FiniteExtension(Poly(x**2 - 2, x, domain=ZZ))
    Ky = FiniteExtension(Poly(y**2 - 2, y, domain=ZZ))
    Kxy = FiniteExtension(Poly(y**2 - 2, y, domain=Kx))
    assert Kx.unify(Kx) == Kx
    assert Ky.unify(Ky) == Ky
    assert Kx.unify(Ky) == Kxy
    assert Ky.unify(Kx) == Kxy

