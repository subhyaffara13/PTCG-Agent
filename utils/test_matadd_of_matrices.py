
def test_matadd_of_matrices():
    assert MatAdd(eye(2), 4*eye(2), eye(2)).doit() == ImmutableMatrix(6*eye(2))
    assert add(eye(2), 4*eye(2), eye(2)).doit() == ImmutableMatrix(6*eye(2))

