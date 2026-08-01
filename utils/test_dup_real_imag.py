
def test_dup_real_imag():
    assert dup_real_imag([], ZZ) == ([[]], [[]])
    assert dup_real_imag([1], ZZ) == ([[1]], [[]])

    assert dup_real_imag([1, 1], ZZ) == ([[1], [1]], [[1, 0]])
    assert dup_real_imag([1, 2], ZZ) == ([[1], [2]], [[1, 0]])

    assert dup_real_imag(
        [1, 2, 3], ZZ) == ([[1], [2], [-1, 0, 3]], [[2, 0], [2, 0]])

    assert dup_real_imag([ZZ(1), ZZ(0), ZZ(1), ZZ(3)], ZZ) == (
        [[ZZ(1)], [], [ZZ(-3), ZZ(0), ZZ(1)], [ZZ(3)]],
        [[ZZ(3), ZZ(0)], [], [ZZ(-1), ZZ(0), ZZ(1), ZZ(0)]]
    )

    raises(DomainError, lambda: dup_real_imag([EX(1), EX(2)], EX))

