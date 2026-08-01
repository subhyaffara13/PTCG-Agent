
def test_issue_14489():
    from sympy.core.mod import Mod
    A = Matrix([-1, 1, 2])
    B = Matrix([10, 20, -15])

    assert Mod(A, 3) == Matrix([2, 1, 2])
    assert Mod(B, 4) == Matrix([2, 0, 1])


def test_issue_14489():
    from sympy.core.mod import Mod
    A = Matrix([-1, 1, 2])
    B = Matrix([10, 20, -15])

    assert Mod(A, 3) == Matrix([2, 1, 2])
    assert Mod(B, 4) == Matrix([2, 0, 1])

