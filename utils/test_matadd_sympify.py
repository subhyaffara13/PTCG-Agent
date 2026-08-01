
def test_matadd_sympify():
    assert isinstance(MatAdd(eye(1), eye(1)).args[0], Basic)
    assert isinstance(add(eye(1), eye(1)).args[0], Basic)

