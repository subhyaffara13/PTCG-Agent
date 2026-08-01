
def test_is_Identity():
    assert eye_Properties(3).is_Identity
    assert not PropertiesOnlyMatrix(zeros(3)).is_Identity
    assert not PropertiesOnlyMatrix(ones(3)).is_Identity
    # issue 6242
    assert not PropertiesOnlyMatrix([[1, 0, 0]]).is_Identity


def test_is_Identity():
    assert eye(3).is_Identity
    assert eye(3).as_immutable().is_Identity
    assert not zeros(3).is_Identity
    assert not ones(3).is_Identity
    # issue 6242
    assert not Matrix([[1, 0, 0]]).is_Identity
    # issue 8854
    assert SparseMatrix(3,3, {(0,0):1, (1,1):1, (2,2):1}).is_Identity
    assert not SparseMatrix(2,3, range(6)).is_Identity
    assert not SparseMatrix(3,3, {(0,0):1, (1,1):1}).is_Identity
    assert not SparseMatrix(3,3, {(0,0):1, (1,1):1, (2,2):1, (0,1):2, (0,2):3}).is_Identity


def test_is_Identity():
    assert eye(3).is_Identity
    assert eye(3).as_immutable().is_Identity
    assert not zeros(3).is_Identity
    assert not ones(3).is_Identity
    # issue 6242
    assert not Matrix([[1, 0, 0]]).is_Identity
    # issue 8854
    assert SparseMatrix(3,3, {(0,0):1, (1,1):1, (2,2):1}).is_Identity
    assert not SparseMatrix(2,3, range(6)).is_Identity
    assert not SparseMatrix(3,3, {(0,0):1, (1,1):1}).is_Identity
    assert not SparseMatrix(3,3, {(0,0):1, (1,1):1, (2,2):1, (0,1):2, (0,2):3}).is_Identity

