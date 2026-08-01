
def test_KSY_precondition():
    """Tests precondition for KSY Resultant."""
    A, B, C = symbols('A, B, C')

    m1 = Matrix([[1, 2, 3],
                 [4, 5, 12],
                 [6, 7, 18]])

    m2 = Matrix([[0, C**2],
                 [-2 * C, -C ** 2]])

    m3 = Matrix([[1, 0],
                 [0, 1]])

    m4 = Matrix([[A**2, 0, 1],
                 [A, 1, 1 / A]])

    m5 = Matrix([[5, 1],
                 [2, B],
                 [0, 1],
                 [0, 0]])

    assert dixon.KSY_precondition(m1) == False
    assert dixon.KSY_precondition(m2) == True
    assert dixon.KSY_precondition(m3) == True
    assert dixon.KSY_precondition(m4) == False
    assert dixon.KSY_precondition(m5) == True

