
def test_definite():
    # Examples from Gilbert Strang, "Introduction to Linear Algebra"
    # Positive definite matrices
    m = Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    assert m.is_positive_definite == True
    assert m.is_positive_semidefinite == True
    assert m.is_negative_definite == False
    assert m.is_negative_semidefinite == False
    assert m.is_indefinite == False

    m = Matrix([[5, 4], [4, 5]])
    assert m.is_positive_definite == True
    assert m.is_positive_semidefinite == True
    assert m.is_negative_definite == False
    assert m.is_negative_semidefinite == False
    assert m.is_indefinite == False

    # Positive semidefinite matrices
    m = Matrix([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]])
    assert m.is_positive_definite == False
    assert m.is_positive_semidefinite == True
    assert m.is_negative_definite == False
    assert m.is_negative_semidefinite == False
    assert m.is_indefinite == False

    m = Matrix([[1, 2], [2, 4]])
    assert m.is_positive_definite == False
    assert m.is_positive_semidefinite == True
    assert m.is_negative_definite == False
    assert m.is_negative_semidefinite == False
    assert m.is_indefinite == False

    # Examples from Mathematica documentation
    # Non-hermitian positive definite matrices
    m = Matrix([[2, 3], [4, 8]])
    assert m.is_positive_definite == True
    assert m.is_positive_semidefinite == True
    assert m.is_negative_definite == False
    assert m.is_negative_semidefinite == False
    assert m.is_indefinite == False

    # Hermetian matrices
    m = Matrix([[1, 2*I], [-I, 4]])
    assert m.is_positive_definite == True
    assert m.is_positive_semidefinite == True
    assert m.is_negative_definite == False
    assert m.is_negative_semidefinite == False
    assert m.is_indefinite == False

    # Symbolic matrices examples
    a = Symbol('a', positive=True)
    b = Symbol('b', negative=True)
    m = Matrix([[a, 0, 0], [0, a, 0], [0, 0, a]])
    assert m.is_positive_definite == True
    assert m.is_positive_semidefinite == True
    assert m.is_negative_definite == False
    assert m.is_negative_semidefinite == False
    assert m.is_indefinite == False

    m = Matrix([[b, 0, 0], [0, b, 0], [0, 0, b]])
    assert m.is_positive_definite == False
    assert m.is_positive_semidefinite == False
    assert m.is_negative_definite == True
    assert m.is_negative_semidefinite == True
    assert m.is_indefinite == False

    m = Matrix([[a, 0], [0, b]])
    assert m.is_positive_definite == False
    assert m.is_positive_semidefinite == False
    assert m.is_negative_definite == False
    assert m.is_negative_semidefinite == False
    assert m.is_indefinite == True

    m = Matrix([
        [0.0228202735623867, 0.00518748979085398,
         -0.0743036351048907, -0.00709135324903921],
        [0.00518748979085398, 0.0349045359786350,
         0.0830317991056637, 0.00233147902806909],
        [-0.0743036351048907, 0.0830317991056637,
         1.15859676366277, 0.340359081555988],
        [-0.00709135324903921, 0.00233147902806909,
         0.340359081555988, 0.928147644848199]
    ])
    assert m.is_positive_definite == True
    assert m.is_positive_semidefinite == True
    assert m.is_indefinite == False

    # test for issue 19547: https://github.com/sympy/sympy/issues/19547
    m = Matrix([
        [0, 0, 0],
        [0, 1, 2],
        [0, 2, 1]
    ])
    assert not m.is_positive_definite
    assert not m.is_positive_semidefinite

