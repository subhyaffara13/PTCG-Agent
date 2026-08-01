
def test_Domain_unify_composite():
    assert unify(ZZ.poly_ring(x), ZZ) == ZZ.poly_ring(x)
    assert unify(ZZ.poly_ring(x), QQ) == QQ.poly_ring(x)
    assert unify(QQ.poly_ring(x), ZZ) == QQ.poly_ring(x)
    assert unify(QQ.poly_ring(x), QQ) == QQ.poly_ring(x)

    assert unify(ZZ, ZZ.poly_ring(x)) == ZZ.poly_ring(x)
    assert unify(QQ, ZZ.poly_ring(x)) == QQ.poly_ring(x)
    assert unify(ZZ, QQ.poly_ring(x)) == QQ.poly_ring(x)
    assert unify(QQ, QQ.poly_ring(x)) == QQ.poly_ring(x)

    assert unify(ZZ.poly_ring(x, y), ZZ) == ZZ.poly_ring(x, y)
    assert unify(ZZ.poly_ring(x, y), QQ) == QQ.poly_ring(x, y)
    assert unify(QQ.poly_ring(x, y), ZZ) == QQ.poly_ring(x, y)
    assert unify(QQ.poly_ring(x, y), QQ) == QQ.poly_ring(x, y)

    assert unify(ZZ, ZZ.poly_ring(x, y)) == ZZ.poly_ring(x, y)
    assert unify(QQ, ZZ.poly_ring(x, y)) == QQ.poly_ring(x, y)
    assert unify(ZZ, QQ.poly_ring(x, y)) == QQ.poly_ring(x, y)
    assert unify(QQ, QQ.poly_ring(x, y)) == QQ.poly_ring(x, y)

    assert unify(ZZ.frac_field(x), ZZ) == ZZ.frac_field(x)
    assert unify(ZZ.frac_field(x), QQ) == QQ.frac_field(x)
    assert unify(QQ.frac_field(x), ZZ) == QQ.frac_field(x)
    assert unify(QQ.frac_field(x), QQ) == QQ.frac_field(x)

    assert unify(ZZ, ZZ.frac_field(x)) == ZZ.frac_field(x)
    assert unify(QQ, ZZ.frac_field(x)) == QQ.frac_field(x)
    assert unify(ZZ, QQ.frac_field(x)) == QQ.frac_field(x)
    assert unify(QQ, QQ.frac_field(x)) == QQ.frac_field(x)

    assert unify(ZZ.frac_field(x, y), ZZ) == ZZ.frac_field(x, y)
    assert unify(ZZ.frac_field(x, y), QQ) == QQ.frac_field(x, y)
    assert unify(QQ.frac_field(x, y), ZZ) == QQ.frac_field(x, y)
    assert unify(QQ.frac_field(x, y), QQ) == QQ.frac_field(x, y)

    assert unify(ZZ, ZZ.frac_field(x, y)) == ZZ.frac_field(x, y)
    assert unify(QQ, ZZ.frac_field(x, y)) == QQ.frac_field(x, y)
    assert unify(ZZ, QQ.frac_field(x, y)) == QQ.frac_field(x, y)
    assert unify(QQ, QQ.frac_field(x, y)) == QQ.frac_field(x, y)

    assert unify(ZZ.poly_ring(x), ZZ.poly_ring(x)) == ZZ.poly_ring(x)
    assert unify(ZZ.poly_ring(x), QQ.poly_ring(x)) == QQ.poly_ring(x)
    assert unify(QQ.poly_ring(x), ZZ.poly_ring(x)) == QQ.poly_ring(x)
    assert unify(QQ.poly_ring(x), QQ.poly_ring(x)) == QQ.poly_ring(x)

    assert unify(ZZ.poly_ring(x, y), ZZ.poly_ring(x)) == ZZ.poly_ring(x, y)
    assert unify(ZZ.poly_ring(x, y), QQ.poly_ring(x)) == QQ.poly_ring(x, y)
    assert unify(QQ.poly_ring(x, y), ZZ.poly_ring(x)) == QQ.poly_ring(x, y)
    assert unify(QQ.poly_ring(x, y), QQ.poly_ring(x)) == QQ.poly_ring(x, y)

    assert unify(ZZ.poly_ring(x), ZZ.poly_ring(x, y)) == ZZ.poly_ring(x, y)
    assert unify(ZZ.poly_ring(x), QQ.poly_ring(x, y)) == QQ.poly_ring(x, y)
    assert unify(QQ.poly_ring(x), ZZ.poly_ring(x, y)) == QQ.poly_ring(x, y)
    assert unify(QQ.poly_ring(x), QQ.poly_ring(x, y)) == QQ.poly_ring(x, y)

    assert unify(ZZ.poly_ring(x, y), ZZ.poly_ring(x, z)) == ZZ.poly_ring(x, y, z)
    assert unify(ZZ.poly_ring(x, y), QQ.poly_ring(x, z)) == QQ.poly_ring(x, y, z)
    assert unify(QQ.poly_ring(x, y), ZZ.poly_ring(x, z)) == QQ.poly_ring(x, y, z)
    assert unify(QQ.poly_ring(x, y), QQ.poly_ring(x, z)) == QQ.poly_ring(x, y, z)

    assert unify(ZZ.frac_field(x), ZZ.frac_field(x)) == ZZ.frac_field(x)
    assert unify(ZZ.frac_field(x), QQ.frac_field(x)) == QQ.frac_field(x)
    assert unify(QQ.frac_field(x), ZZ.frac_field(x)) == QQ.frac_field(x)
    assert unify(QQ.frac_field(x), QQ.frac_field(x)) == QQ.frac_field(x)

    assert unify(ZZ.frac_field(x, y), ZZ.frac_field(x)) == ZZ.frac_field(x, y)
    assert unify(ZZ.frac_field(x, y), QQ.frac_field(x)) == QQ.frac_field(x, y)
    assert unify(QQ.frac_field(x, y), ZZ.frac_field(x)) == QQ.frac_field(x, y)
    assert unify(QQ.frac_field(x, y), QQ.frac_field(x)) == QQ.frac_field(x, y)

    assert unify(ZZ.frac_field(x), ZZ.frac_field(x, y)) == ZZ.frac_field(x, y)
    assert unify(ZZ.frac_field(x), QQ.frac_field(x, y)) == QQ.frac_field(x, y)
    assert unify(QQ.frac_field(x), ZZ.frac_field(x, y)) == QQ.frac_field(x, y)
    assert unify(QQ.frac_field(x), QQ.frac_field(x, y)) == QQ.frac_field(x, y)

    assert unify(ZZ.frac_field(x, y), ZZ.frac_field(x, z)) == ZZ.frac_field(x, y, z)
    assert unify(ZZ.frac_field(x, y), QQ.frac_field(x, z)) == QQ.frac_field(x, y, z)
    assert unify(QQ.frac_field(x, y), ZZ.frac_field(x, z)) == QQ.frac_field(x, y, z)
    assert unify(QQ.frac_field(x, y), QQ.frac_field(x, z)) == QQ.frac_field(x, y, z)

    assert unify(ZZ.poly_ring(x), ZZ.frac_field(x)) == ZZ.frac_field(x)
    assert unify(ZZ.poly_ring(x), QQ.frac_field(x)) == ZZ.frac_field(x)
    assert unify(QQ.poly_ring(x), ZZ.frac_field(x)) == ZZ.frac_field(x)
    assert unify(QQ.poly_ring(x), QQ.frac_field(x)) == QQ.frac_field(x)

    assert unify(ZZ.poly_ring(x, y), ZZ.frac_field(x)) == ZZ.frac_field(x, y)
    assert unify(ZZ.poly_ring(x, y), QQ.frac_field(x)) == ZZ.frac_field(x, y)
    assert unify(QQ.poly_ring(x, y), ZZ.frac_field(x)) == ZZ.frac_field(x, y)
    assert unify(QQ.poly_ring(x, y), QQ.frac_field(x)) == QQ.frac_field(x, y)

    assert unify(ZZ.poly_ring(x), ZZ.frac_field(x, y)) == ZZ.frac_field(x, y)
    assert unify(ZZ.poly_ring(x), QQ.frac_field(x, y)) == ZZ.frac_field(x, y)
    assert unify(QQ.poly_ring(x), ZZ.frac_field(x, y)) == ZZ.frac_field(x, y)
    assert unify(QQ.poly_ring(x), QQ.frac_field(x, y)) == QQ.frac_field(x, y)

    assert unify(ZZ.poly_ring(x, y), ZZ.frac_field(x, z)) == ZZ.frac_field(x, y, z)
    assert unify(ZZ.poly_ring(x, y), QQ.frac_field(x, z)) == ZZ.frac_field(x, y, z)
    assert unify(QQ.poly_ring(x, y), ZZ.frac_field(x, z)) == ZZ.frac_field(x, y, z)
    assert unify(QQ.poly_ring(x, y), QQ.frac_field(x, z)) == QQ.frac_field(x, y, z)

    assert unify(ZZ.frac_field(x), ZZ.poly_ring(x)) == ZZ.frac_field(x)
    assert unify(ZZ.frac_field(x), QQ.poly_ring(x)) == ZZ.frac_field(x)
    assert unify(QQ.frac_field(x), ZZ.poly_ring(x)) == ZZ.frac_field(x)
    assert unify(QQ.frac_field(x), QQ.poly_ring(x)) == QQ.frac_field(x)

    assert unify(ZZ.frac_field(x, y), ZZ.poly_ring(x)) == ZZ.frac_field(x, y)
    assert unify(ZZ.frac_field(x, y), QQ.poly_ring(x)) == ZZ.frac_field(x, y)
    assert unify(QQ.frac_field(x, y), ZZ.poly_ring(x)) == ZZ.frac_field(x, y)
    assert unify(QQ.frac_field(x, y), QQ.poly_ring(x)) == QQ.frac_field(x, y)

    assert unify(ZZ.frac_field(x), ZZ.poly_ring(x, y)) == ZZ.frac_field(x, y)
    assert unify(ZZ.frac_field(x), QQ.poly_ring(x, y)) == ZZ.frac_field(x, y)
    assert unify(QQ.frac_field(x), ZZ.poly_ring(x, y)) == ZZ.frac_field(x, y)
    assert unify(QQ.frac_field(x), QQ.poly_ring(x, y)) == QQ.frac_field(x, y)

    assert unify(ZZ.frac_field(x, y), ZZ.poly_ring(x, z)) == ZZ.frac_field(x, y, z)
    assert unify(ZZ.frac_field(x, y), QQ.poly_ring(x, z)) == ZZ.frac_field(x, y, z)
    assert unify(QQ.frac_field(x, y), ZZ.poly_ring(x, z)) == ZZ.frac_field(x, y, z)
    assert unify(QQ.frac_field(x, y), QQ.poly_ring(x, z)) == QQ.frac_field(x, y, z)

