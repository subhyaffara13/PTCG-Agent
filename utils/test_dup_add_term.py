
def test_dup_add_term():
    f = dup_normal([], ZZ)

    assert dup_add_term(f, ZZ(0), 0, ZZ) == dup_normal([], ZZ)

    assert dup_add_term(f, ZZ(1), 0, ZZ) == dup_normal([1], ZZ)
    assert dup_add_term(f, ZZ(1), 1, ZZ) == dup_normal([1, 0], ZZ)
    assert dup_add_term(f, ZZ(1), 2, ZZ) == dup_normal([1, 0, 0], ZZ)

    f = dup_normal([1, 1, 1], ZZ)

    assert dup_add_term(f, ZZ(1), 0, ZZ) == dup_normal([1, 1, 2], ZZ)
    assert dup_add_term(f, ZZ(1), 1, ZZ) == dup_normal([1, 2, 1], ZZ)
    assert dup_add_term(f, ZZ(1), 2, ZZ) == dup_normal([2, 1, 1], ZZ)

    assert dup_add_term(f, ZZ(1), 3, ZZ) == dup_normal([1, 1, 1, 1], ZZ)
    assert dup_add_term(f, ZZ(1), 4, ZZ) == dup_normal([1, 0, 1, 1, 1], ZZ)
    assert dup_add_term(f, ZZ(1), 5, ZZ) == dup_normal([1, 0, 0, 1, 1, 1], ZZ)
    assert dup_add_term(
        f, ZZ(1), 6, ZZ) == dup_normal([1, 0, 0, 0, 1, 1, 1], ZZ)

    assert dup_add_term(f, ZZ(-1), 2, ZZ) == dup_normal([1, 1], ZZ)

