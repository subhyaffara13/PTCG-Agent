
def test_issue_10589():
    x, y, z = symbols("x, y z")
    M1 = Matrix([x, y, z])
    M1 = M1.subs(zip([x, y, z], [1, 2, 3]))
    assert M1 == Matrix([[1], [2], [3]])

    M2 = Matrix([[x, x, x, x, x], [x, x, x, x, x], [x, x, x, x, x]])
    M2 = M2.subs(zip([x], [1]))
    assert M2 == Matrix([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])


def test_issue_10589():
    x, y, z = symbols("x, y z")
    M1 = Matrix([x, y, z])
    M1 = M1.subs(zip([x, y, z], [1, 2, 3]))
    assert M1 == Matrix([[1], [2], [3]])

    M2 = Matrix([[x, x, x, x, x], [x, x, x, x, x], [x, x, x, x, x]])
    M2 = M2.subs(zip([x], [1]))
    assert M2 == Matrix([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])

