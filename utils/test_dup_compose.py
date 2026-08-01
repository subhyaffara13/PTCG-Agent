
def test_dup_compose():
    assert dup_compose([], [], ZZ) == []
    assert dup_compose([], [1], ZZ) == []
    assert dup_compose([], [1, 2], ZZ) == []

    assert dup_compose([1], [], ZZ) == [1]

    assert dup_compose([1, 2, 0], [], ZZ) == []
    assert dup_compose([1, 2, 1], [], ZZ) == [1]

    assert dup_compose([1, 2, 1], [1], ZZ) == [4]
    assert dup_compose([1, 2, 1], [7], ZZ) == [64]

    assert dup_compose([1, 2, 1], [1, -1], ZZ) == [1, 0, 0]
    assert dup_compose([1, 2, 1], [1, 1], ZZ) == [1, 4, 4]
    assert dup_compose([1, 2, 1], [1, 2, 1], ZZ) == [1, 4, 8, 8, 4]

