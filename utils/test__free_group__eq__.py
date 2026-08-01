
def test_FreeGroup__eq__():
    assert free_group("x, y, z")[0] == free_group("x, y, z")[0]
    assert free_group("x, y, z")[0] is free_group("x, y, z")[0]

    assert free_group("x, y, z")[0] != free_group("a, x, y")[0]
    assert free_group("x, y, z")[0] is not free_group("a, x, y")[0]

    assert free_group("x, y")[0] != free_group("x, y, z")[0]
    assert free_group("x, y")[0] is not free_group("x, y, z")[0]

    assert free_group("x, y, z")[0] != free_group("x, y")[0]
    assert free_group("x, y, z")[0] is not free_group("x, y")[0]

