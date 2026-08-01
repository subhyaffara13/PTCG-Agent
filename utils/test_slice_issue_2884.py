
def test_slice_issue_2884():
    m = Matrix(2, 2, range(4))
    assert m[1, :] == Matrix([[2, 3]])
    assert m[-1, :] == Matrix([[2, 3]])
    assert m[:, 1] == Matrix([[1, 3]]).T
    assert m[:, -1] == Matrix([[1, 3]]).T
    raises(IndexError, lambda: m[2, :])
    raises(IndexError, lambda: m[2, 2])


def test_slice_issue_2884():
    m = Matrix(2, 2, range(4))
    assert m[1, :] == Matrix([[2, 3]])
    assert m[-1, :] == Matrix([[2, 3]])
    assert m[:, 1] == Matrix([[1, 3]]).T
    assert m[:, -1] == Matrix([[1, 3]]).T
    raises(IndexError, lambda: m[2, :])
    raises(IndexError, lambda: m[2, 2])

