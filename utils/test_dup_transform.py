
def test_dup_transform():
    assert dup_transform([], [], [1, 1], ZZ) == []
    assert dup_transform([], [1], [1, 1], ZZ) == []
    assert dup_transform([], [1, 2], [1, 1], ZZ) == []

    assert dup_transform([6, -5, 4, -3, 17], [1, -3, 4], [2, -3], ZZ) == \
        [6, -82, 541, -2205, 6277, -12723, 17191, -13603, 4773]

