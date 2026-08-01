
def test_sympy__physics__control__lti__StateSpace():
    from sympy.matrices.dense import Matrix
    from sympy.physics.control import StateSpace
    A = Matrix([[-5, -1], [3, -1]])
    B = Matrix([2, 5])
    C = Matrix([[1, 2]])
    D = Matrix([0])
    assert _test_args(StateSpace(A, B, C, D))

