
def test_dmp_exquo_ground():
    f = dmp_normal([[6], [2], [8]], 1, ZZ)

    assert dmp_exquo_ground(f, ZZ(1), 1, ZZ) == f
    assert dmp_exquo_ground(
        f, ZZ(2), 1, ZZ) == dmp_normal([[3], [1], [4]], 1, ZZ)

