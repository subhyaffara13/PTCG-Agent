
def test_dup_l1_norm():
    assert dup_l1_norm([], ZZ) == 0
    assert dup_l1_norm([1], ZZ) == 1
    assert dup_l1_norm([1, 4, 2, 3], ZZ) == 10

