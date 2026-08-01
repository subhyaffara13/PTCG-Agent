
def test_creation_args():
    """
    Check that matrix dimensions can be specified using any reasonable type
    (see issue 4614).
    """
    raises(ValueError, lambda: zeros(3, -1))
    raises(TypeError, lambda: zeros(1, 2, 3, 4))
    assert zeros(int(3)) == zeros(3)
    assert zeros(Integer(3)) == zeros(3)
    raises(ValueError, lambda: zeros(3.))
    assert eye(int(3)) == eye(3)
    assert eye(Integer(3)) == eye(3)
    raises(ValueError, lambda: eye(3.))
    assert ones(int(3), Integer(4)) == ones(3, 4)
    raises(TypeError, lambda: Matrix(5))
    raises(TypeError, lambda: Matrix(1, 2))
    raises(ValueError, lambda: Matrix([1, [2]]))


def test_creation_args():
    """
    Check that matrix dimensions can be specified using any reasonable type
    (see issue 4614).
    """
    raises(ValueError, lambda: zeros(3, -1))
    raises(TypeError, lambda: zeros(1, 2, 3, 4))
    assert zeros(int(3)) == zeros(3)
    assert zeros(Integer(3)) == zeros(3)
    raises(ValueError, lambda: zeros(3.))
    assert eye(int(3)) == eye(3)
    assert eye(Integer(3)) == eye(3)
    raises(ValueError, lambda: eye(3.))
    assert ones(int(3), Integer(4)) == ones(3, 4)
    raises(TypeError, lambda: Matrix(5))
    raises(TypeError, lambda: Matrix(1, 2))
    raises(ValueError, lambda: Matrix([1, [2]]))

