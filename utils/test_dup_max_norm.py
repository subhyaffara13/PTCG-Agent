
def test_dup_max_norm():
    assert dup_max_norm([], ZZ) == 0
    assert dup_max_norm([1], ZZ) == 1

    assert dup_max_norm([1, 4, 2, 3], ZZ) == 4

