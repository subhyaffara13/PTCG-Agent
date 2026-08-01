
def test_dup_mul_ground():
    f = dup_normal([], ZZ)

    assert dup_mul_ground(f, ZZ(2), ZZ) == dup_normal([], ZZ)

    f = dup_normal([1, 2, 3], ZZ)

    assert dup_mul_ground(f, ZZ(0), ZZ) == dup_normal([], ZZ)
    assert dup_mul_ground(f, ZZ(2), ZZ) == dup_normal([2, 4, 6], ZZ)

