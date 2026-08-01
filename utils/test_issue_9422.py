
def test_issue_9422():
    x, y = symbols('x y', commutative=False)
    a, b = symbols('a b')
    M = eye(2)
    M1 = Matrix(2, 2, [x, y, y, z])
    assert y*x*M != x*y*M
    assert b*a*M == a*b*M
    assert x*M1 != M1*x
    assert a*M1 == M1*a
    assert y*x*M == Matrix([[y*x, 0], [0, y*x]])


def test_issue_9422():
    x, y = symbols('x y', commutative=False)
    a, b = symbols('a b')
    M = eye(2)
    M1 = Matrix(2, 2, [x, y, y, z])
    assert y*x*M != x*y*M
    assert b*a*M == a*b*M
    assert x*M1 != M1*x
    assert a*M1 == M1*a
    assert y*x*M == Matrix([[y*x, 0], [0, y*x]])

